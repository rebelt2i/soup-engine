#!/usr/bin/env python3
"""
Pack per-body Soup Engine release zips for GitHub Releases.

Expects builds already done:

  Classic (5DC.111):
    card/AUTOEXEC.BIN, card/SE.BIN   (or --classic-dir)

  Film-in-ML (50D.109, 6D.116, 5D3.123, 550D.109):
    src/vendor/magiclantern/platform/<PLATFORM>/build/autoexec.bin
    src/vendor/magiclantern/platform/<PLATFORM>/build/<MODEL>_<FW>.sym

Writes dist/soup-engine-<tag>-<PLATFORM>.zip with LICENSE, NOTICE,
INSTALL.txt, AUTOEXEC.BIN, stocks, and SE.BIN / .sym as required.

  python3 tools/pack-release.py --tag v0.2.0-beta
  python3 tools/pack-release.py --tag v0.2.0-beta --platforms 50D.109
"""

from __future__ import print_function

import argparse
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC)
STOCKS = os.path.join(SRC, "stocks")
CARD = os.path.join(ROOT, "card")
ML_BUILD = os.path.join(SRC, "vendor", "magiclantern", "platform")
DIST = os.path.join(ROOT, "dist")

CLASSIC = ("5DC.111",)
FILM_ML = ("50D.109", "6D.116", "5D3.123", "550D.109")
ALL = CLASSIC + FILM_ML

# Photographer-facing names for INSTALL.txt
BODY = {
    "5DC.111": {
        "title": "EOS 5D Classic",
        "firmware": "1.1.1",
        "ml": "https://builds.magiclantern.fm/5DC.html",
        "ui": "Trash-button film picker (Magic Lantern menu is replaced).",
        "family": "classic",
    },
    "50D.109": {
        "title": "EOS 50D",
        "firmware": "1.0.9",
        "ml": "https://builds.magiclantern.fm/50D.html",
        "ui": "Magic Lantern menu → Film page (F tab).",
        "family": "film-ml",
    },
    "6D.116": {
        "title": "EOS 6D Mark I",
        "firmware": "1.1.6",
        "ml": "https://builds.magiclantern.fm/6D.html",
        "ui": "Magic Lantern menu → Film page (F tab).",
        "family": "film-ml",
    },
    "5D3.123": {
        "title": "EOS 5D Mark III",
        "firmware": "1.2.3",
        "ml": "https://builds.magiclantern.fm/5D3.html",
        "ui": "Magic Lantern menu → Film page (F tab).",
        "family": "film-ml",
    },
    "550D.109": {
        "title": "EOS 550D",
        "firmware": "1.0.9",
        "ml": "https://builds.magiclantern.fm/550D.html",
        "ui": "Magic Lantern menu → Film page (F tab).",
        "family": "film-ml",
    },
}


def die(msg):
    sys.stderr.write("pack-release: %s\n" % msg)
    raise SystemExit(1)


def sym_name(platform):
    model, fw = platform.split(".", 1)
    return "%s_%s.sym" % (model, fw)


def install_txt(platform, tag):
    info = BODY[platform]
    lines = [
        "Soup Engine %s - %s (firmware %s)"
        % (tag, info["title"], info["firmware"]),
        "",
        "Beta. Unofficial. No warranty. See LICENSE and NOTICE.",
        "",
        "1. Install stock Magic Lantern for this firmware first:",
        "   %s" % info["ml"],
        "   Confirm the camera boots and the ML menu opens.",
        "",
        "2. Back up the stock AUTOEXEC.BIN from the card",
    ]
    if info["family"] == "film-ml":
        lines.append(
            "   and the matching ML/modules/%s file." % sym_name(platform)
        )
    else:
        lines.append("   somewhere safe. Putting it back uninstalls Soup Engine.")
    lines.extend([
        "",
        "3. Unzip this archive to the root of the card",
        "   (same place as AUTOEXEC.BIN). Replace when asked.",
        "",
        "4. Put the card in the camera and switch on.",
        "   %s" % info["ui"],
    ])
    if info["family"] == "film-ml":
        lines.extend([
            "   Turn Film on. Leave Delete CR2 off until you like a look.",
        ])
    lines.extend([
        "",
        "Picture Style: Standard, Neutral, or Faithful (not Monochrome).",
        "",
        "Corresponding source: tag %s of" % tag,
        "https://github.com/rebelt2i/soup-engine",
        "",
        "Not affiliated with Canon, Fujifilm, Kodak, Adobe, or Magic Lantern.",
        "Film names are trademarks of their owners.",
    ])
    return "\n".join(lines) + "\n"


def copy_stocks(dest_film):
    os.makedirs(dest_film, exist_ok=True)
    if not os.path.isdir(STOCKS):
        die("missing stocks at %s" % STOCKS)
    n = 0
    for name in sorted(os.listdir(STOCKS)):
        if name.endswith(".fs") or name == "INDEX.TXT":
            shutil.copy2(os.path.join(STOCKS, name),
                         os.path.join(dest_film, name))
            n += 1
    if n < 2:
        die("expected .fs stocks and INDEX.TXT under %s" % STOCKS)


def require_file(path, label):
    if not os.path.isfile(path):
        die("missing %s: %s" % (label, path))
    return path


def stage_classic(staging, classic_dir):
    auto = require_file(os.path.join(classic_dir, "AUTOEXEC.BIN"),
                        "Classic AUTOEXEC.BIN")
    se = require_file(os.path.join(classic_dir, "SE.BIN"), "Classic SE.BIN")
    shutil.copy2(auto, os.path.join(staging, "AUTOEXEC.BIN"))
    shutil.copy2(se, os.path.join(staging, "SE.BIN"))
    copy_stocks(os.path.join(staging, "ML", "FILM"))


def stage_film_ml(staging, platform, build_root):
    plat_build = os.path.join(build_root, platform, "build")
    auto = require_file(os.path.join(plat_build, "autoexec.bin"),
                        "%s autoexec.bin" % platform)
    sym = require_file(os.path.join(plat_build, sym_name(platform)),
                       "%s sym" % platform)
    shutil.copy2(auto, os.path.join(staging, "AUTOEXEC.BIN"))
    mod = os.path.join(staging, "ML", "modules")
    os.makedirs(mod, exist_ok=True)
    shutil.copy2(sym, os.path.join(mod, os.path.basename(sym)))
    copy_stocks(os.path.join(staging, "ML", "FILM"))


def add_tree(zf, staging):
    for dirpath, _dirs, files in os.walk(staging):
        for name in files:
            full = os.path.join(dirpath, name)
            arc = os.path.relpath(full, staging).replace("\\", "/")
            zf.write(full, arc)


def pack_one(platform, tag, classic_dir, ml_build, dist):
    info = BODY[platform]
    staging = os.path.join(dist, "_stage_%s" % platform)
    if os.path.isdir(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    if info["family"] == "classic":
        stage_classic(staging, classic_dir)
    else:
        stage_film_ml(staging, platform, ml_build)

    for name in ("LICENSE", "NOTICE"):
        src = os.path.join(ROOT, name)
        require_file(src, name)
        shutil.copy2(src, os.path.join(staging, name))

    with open(os.path.join(staging, "INSTALL.txt"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(install_txt(platform, tag))

    zip_path = os.path.join(dist, "soup-engine-%s-%s.zip" % (tag, platform))
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        add_tree(zf, staging)
    shutil.rmtree(staging)
    sys.stderr.write("wrote %s\n" % zip_path)
    return zip_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tag", required=True,
                    help="release tag, e.g. v0.2.0-beta")
    ap.add_argument("--platforms", nargs="+", choices=ALL, default=list(ALL),
                    help="bodies to pack (default: all release bodies)")
    ap.add_argument("--classic-dir", default=CARD,
                    help="directory with Classic AUTOEXEC.BIN and SE.BIN")
    ap.add_argument("--ml-build", default=ML_BUILD,
                    help="Magic Lantern platform/ tree with build/ outputs")
    ap.add_argument("--dist", default=DIST, help="output directory")
    args = ap.parse_args()

    tag = args.tag.lstrip()
    if not tag:
        die("empty --tag")
    os.makedirs(args.dist, exist_ok=True)

    written = []
    for platform in args.platforms:
        written.append(pack_one(
            platform, tag, args.classic_dir, args.ml_build, args.dist
        ))
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
