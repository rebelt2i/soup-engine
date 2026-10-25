#!/usr/bin/env python3
"""
Build Magic Lantern autoexec with the Soup Film menu for a DryOS body.

The Magic Lantern tree is not part of this repo. This checks out the
pinned commit, copies integrations/magiclantern/_common then the
platform overlay over it, and builds platform/<PLATFORM>. The engine
sources stay in src/engine and the platform Makefile finds them from
that checkout.

    python3 tools/build-ml.py --platform 50D.109
    python3 tools/build-ml.py --platform 6D.116 --card I:\\
    python3 tools/build-ml.py --platform 5D3.123 --card I:\\

Classic bodies (5DC, 40D) use make payload + patch-film.py instead.
"""

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC)
ML_ROOT = os.path.join(ROOT, "integrations", "magiclantern")
COMMON = os.path.join(ML_ROOT, "_common")
ML = os.path.join(SRC, "vendor", "magiclantern")
REMOTE = "https://github.com/reticulatedpines/magiclantern_simplified"

# Platforms that ship via Film-in-ML rebuild (not Classic SE.BIN).
PLATFORMS = ("50D.109", "6D.116", "5D3.123")


def die(msg):
    sys.stderr.write("build-ml: %s\n" % msg)
    raise SystemExit(1)


def run(cmd, cwd=None, env=None):
    sys.stderr.write("+ %s\n" % " ".join(cmd))
    r = subprocess.call(cmd, cwd=cwd, env=env)
    if r != 0:
        die("command failed (%d)" % r)


def overlay_dir(platform):
    return os.path.join(ML_ROOT, platform)


def pin_file(platform):
    return os.path.join(overlay_dir(platform), "SOUP-PIN.txt")


def pin_commit(platform):
    path = pin_file(platform)
    if not os.path.isfile(path):
        die("missing %s" % path)
    for line in open(path, "r", encoding="utf-8"):
        line = line.strip()
        if line.lower().startswith("commit "):
            return line.split()[1]
    die("no Commit line in %s" % path)


def git(args, cwd):
    run(["git"] + args, cwd=cwd)


def ensure_tree(commit):
    if not os.path.isdir(os.path.join(ML, ".git")):
        os.makedirs(os.path.dirname(ML), exist_ok=True)
        run(["git", "clone", REMOTE, ML])
        git(["checkout", "--detach", commit], ML)
    elif not os.path.isfile(os.path.join(ML, "src", "menu.c")):
        git(["fetch", "--depth", "1", "origin", commit], ML)
        git(["checkout", "--detach", "FETCH_HEAD"], ML)


def copy_tree_files(src_root):
    """Copy every file under src_root into ML, preserving relative paths."""
    if not os.path.isdir(src_root):
        die("missing overlay %s" % src_root)
    for dirpath, _dirs, files in os.walk(src_root):
        rel = os.path.relpath(dirpath, src_root)
        for name in files:
            if name == "SOUP-PIN.txt" or name.endswith(".md"):
                continue
            src = os.path.join(dirpath, name)
            dst = os.path.join(ML, rel, name) if rel != "." else os.path.join(ML, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def copy_overlay(platform):
    if not os.path.isdir(COMMON):
        die("missing common overlay %s" % COMMON)
    copy_tree_files(COMMON)
    copy_tree_files(overlay_dir(platform))


def arm_binpath():
    env = os.environ.get("ARM_BINPATH")
    if env and os.path.isfile(os.path.join(env, "arm-none-eabi-gcc")):
        return env
    candidates = [
        r"C:\PROGRA~2\ARMGNU~1\14EFD8~1.2RE\bin",
        "/usr/bin",
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(c, "arm-none-eabi-gcc")) or \
           os.path.isfile(os.path.join(c, "arm-none-eabi-gcc.exe")):
            return c
    die("set ARM_BINPATH to the directory that contains arm-none-eabi-gcc")


def sym_name(platform):
    # 50D.109 -> 50D_109.sym
    model, fw = platform.split(".", 1)
    return "%s_%s.sym" % (model, fw)


def build(platform):
    plat = os.path.join(ML, "platform", platform)
    if not os.path.isdir(plat):
        die("ML tree has no platform/%s after overlay" % platform)
    env = os.environ.copy()
    arm = arm_binpath()
    extra = [arm]
    git_usr = r"C:\Program Files\Git\usr\bin"
    if os.path.isdir(git_usr):
        extra.append(git_usr)
    env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "")])
    sym = sym_name(platform)
    run([
        "make",
        "ARM_BINPATH=" + arm.replace("\\", "/"),
        "PYTHON=" + sys.executable.replace("\\", "/"),
        "build/autoexec.bin",
        "build/" + sym,
    ], cwd=plat, env=env)
    auto = os.path.join(plat, "build", "autoexec.bin")
    sym_path = os.path.join(plat, "build", sym)
    if not os.path.isfile(auto) or not os.path.isfile(sym_path):
        die("build did not produce autoexec.bin and %s" % sym)
    return auto, sym_path


def copy_card(card, auto, sym_path, platform):
    root = card.rstrip("\\/")
    if not os.path.isdir(root):
        die("card not found: %s" % card)
    shutil.copy2(auto, os.path.join(root, "AUTOEXEC.BIN"))
    mod = os.path.join(root, "ML", "modules")
    os.makedirs(mod, exist_ok=True)
    shutil.copy2(sym_path, os.path.join(mod, os.path.basename(sym_path)))
    film = os.path.join(root, "ML", "FILM")
    os.makedirs(film, exist_ok=True)
    stocks = os.path.join(SRC, "stocks")
    for name in os.listdir(stocks):
        if name.endswith(".fs") or name == "INDEX.TXT":
            shutil.copy2(os.path.join(stocks, name), os.path.join(film, name))
    sys.stderr.write(
        "copied AUTOEXEC.BIN, %s, and ML/FILM to %s\n"
        % (os.path.basename(sym_path), root)
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--platform",
        required=True,
        choices=PLATFORMS,
        help="Film-in-ML body to build",
    )
    ap.add_argument("--card", help="copy AUTOEXEC.BIN, the sym, and ML/FILM here")
    args = ap.parse_args()
    platform = args.platform
    commit = pin_commit(platform)
    ensure_tree(commit)
    copy_overlay(platform)
    auto, sym_path = build(platform)
    if args.card:
        copy_card(args.card, auto, sym_path, platform)
    else:
        sys.stderr.write("built %s\nbuilt %s\n" % (auto, sym_path))


if __name__ == "__main__":
    main()
