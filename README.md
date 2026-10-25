<div align="center">

# 🎞️ Soup Engine <sub><sup>beta</sup></sub>

### Film looks, in the camera, on several Canon EOS bodies.

<br>

<img src="doc/camera.gif" alt="scrolling the film stocks on the camera" width="620">

<br>
<br>

`beta` &nbsp;·&nbsp; `GPL v2` &nbsp;·&nbsp; `13 film stocks`

</div>

<br>

The same look engine runs on every supported body. How you install it, and
how you pick a stock, depends on the camera family — see **Installing** and
**Using it** below.

| Camera | Firmware | Install path | UI |
|:--|:--|:--|:--|
| EOS 5D Classic | 1.1.1 | Classic (`SE.BIN` + patch) | Trash-button picker |
| EOS 40D | 1.1.1 | Classic (`SE.BIN` + patch) | Trash-button picker (**experimental**) |
| EOS 50D | 1.0.9 | Film-in-ML rebuild | Magic Lantern **Film** page |
| EOS 6D Mark I | 1.1.6 | Film-in-ML rebuild | Magic Lantern **Film** page |
| EOS 5D Mark III | **1.2.3** | Film-in-ML rebuild | Magic Lantern **Film** page |

```
# Classic (5D Classic, 40D)
IMG_1234.CR2        your raw file, untouched
IMG_1234.FLM.JPG    the same photo with the look on it

# Film-in-ML (50D, 6D, 5D Mark III)
IMG_1234.CR2        your raw file (preview updated when Delete CR2 is off)
FLM_1234.JPG        the same photo with the look on it
```

<br>

![all thirteen film looks on one frame](doc/stocks.jpg)

<div align="center"><sub>
All thirteen, one frame, straight off the card.
</sub></div>

<br>

> ⚠️ **Beta.** Unofficial code on old cameras. It's easy to remove.
> Only the firmwares in the table above are in scope; other bodies and
> firmware versions are not. The **40D** port is experimental: there is no
> official Magic Lantern build, and card I/O must be proven first.

> ⚖️ **No warranty.** Like all GPL software this comes with none. You
> install it at your own risk. See sections 11 and 12 of the
> [licence](LICENSE).

> 🎨 **The looks are still being tweaked** and will keep changing. The
> names are shorthand for the films they're based on, not exact copies.
> All trademarks belong to their owners.

<br>

---

<br>

## 📦 Installing

There are two install families. Steps are **not** interchangeable.

- **Classic** (5D Classic, 40D): patch Magic Lantern's `AUTOEXEC.BIN` and
  boot a separate `SE.BIN`.
- **Film-in-ML** (50D, 6D, 5D Mark III): rebuild Magic Lantern with a Film
  page linked in. No `SE.BIN`. Do **not** run `tools/patch-film.py` on
  these bodies.

<br>

### EOS 5D Classic (firmware 1.1.1)

#### 1️⃣ &nbsp; Install Magic Lantern

> ### 👉 [builds.magiclantern.fm/5DC.html](https://builds.magiclantern.fm/5DC.html)

Follow their instructions, then check the camera starts and their menu
opens before going further. Soup Engine never touches your camera's
boot flag; their installer does that.

<br>

#### 2️⃣ &nbsp; Back up their `autoexec.bin`

Copy it off the card somewhere safe. Putting it back is how you
uninstall.

<br>

#### 3️⃣ &nbsp; Copy the files to the root of your card

> ### 📦 [Download the latest release](https://github.com/jiijii0/soup-engine/releases/latest)

Unzip to the card root, replacing `AUTOEXEC.BIN`. Or copy
[`card/`](card) from this repo, which is the same files.

| file | what it is |
|:--|:--|
| 📄 `AUTOEXEC.BIN` | replaces Magic Lantern's |
| ⚙️ `SE.BIN` | the engine |
| 🎞️ `ML/FILM/` | the film stocks |

<br>

#### ✅ &nbsp; Put the card in and switch the camera on

That's it. Nothing to enable, no menu to find.

> While Soup Engine is installed you won't have Magic Lantern's own
> menu, since this replaces the file that provides it. Put their
> `autoexec.bin` back whenever you want it again.

<br>

### EOS 40D (firmware 1.1.1) — experimental

Same Classic contract as the 5D Classic (VxWorks, trash-button picker).
There is **no** official Magic Lantern page for this body.

1. Obtain a bootable experimental 40D.111 Magic Lantern `autoexec.bin` and
   confirm **FIO works** (card read/write) before anything else.
2. Place it at `src/vendor/magiclantern-40D/autoexec.bin` (see
   [`src/ml/platforms/40D.111/README.md`](src/ml/platforms/40D.111/README.md)).
3. When patch holes are confirmed for that binary:

```sh
make -C src payload PLATFORM=40D.111
python3 src/tools/patch-film.py --platform 40D.111
```

Until `holes_confirmed` is set in that platform's `patch.json`, the patch
tool refuses to run on purpose.

<br>

### EOS 50D / 6D Mark I / 5D Mark III (Film-in-ML)

| Body | Firmware | Magic Lantern | Build |
|:--|:--|:--|:--|
| 50D | 1.0.9 | [50D.html](https://builds.magiclantern.fm/50D.html) | `--platform 50D.109` |
| 6D Mark I | 1.1.6 | [6D.html](https://builds.magiclantern.fm/6D.html) | `--platform 6D.116` |
| 5D Mark III | **1.2.3** | [5D3.html](https://builds.magiclantern.fm/5D3.html) | `--platform 5D3.123` |

<br>

#### 1️⃣ &nbsp; Install stock Magic Lantern for that firmware

Follow their instructions. Confirm the camera starts and the ML menu opens.

<br>

#### 2️⃣ &nbsp; Back up their `autoexec.bin` and matching `.sym`

Putting those back is how you uninstall.

<br>

#### 3️⃣ &nbsp; Build AUTOEXEC with the Film page

```sh
python3 src/tools/build-ml.py --platform 50D.109 --card /path/to/card
python3 src/tools/build-ml.py --platform 6D.116 --card /path/to/card
python3 src/tools/build-ml.py --platform 5D3.123 --card /path/to/card
```

(`build-50d.py` remains a thin wrapper for `50D.109`.)

That checks out Magic Lantern `ed3e7c0d`, overlays
[`integrations/magiclantern/`](integrations/magiclantern/), and writes:

| file | what it is |
|:--|:--|
| 📄 `AUTOEXEC.BIN` | Magic Lantern, with the Film page linked in |
| 📄 `ML/modules/<MODEL>_<FW>.sym` | must match that `AUTOEXEC.BIN` |
| 🎞️ `ML/FILM/` | the film stocks |

Why the Classic patch path fails on the 50D is in
[`src/ml/platforms/50D.109/PITFALLS.md`](src/ml/platforms/50D.109/PITFALLS.md).

<br>

#### ✅ &nbsp; Put the card in and switch the camera on

Open the Magic Lantern menu. The **Film** page is the one with the `F`
tab. Turn **Film** on. Leave **Delete CR2** off until you have seen a
picture you like.

<br>

---

<br>

## 📷 Using it

<br>

### Classic (5D Classic, 40D)

Press the **trash button** and the picker fills the screen.

| button | what it does |
|:--|:--|
| 🎛️ **Wheel** | choose a film |
| ↕️ **Up / Down** | choose where the look comes from |
| ✅ **`SET`** | pick that film and close |
| 🗑️ **Trash** | close, changing nothing |

Your choice survives switching the camera off.

Each photo takes about twenty seconds to develop. You can keep shooting
while it works, and the screen shows `FRAME 2 OF 3` when there's a
queue.

<br>

> ### ⚠️ Set your Picture Style to Standard, Neutral or Faithful
>
> On Monochrome every look comes out black and white.

<br>

**`SOURCE: JPEG`** is the default. Use this.

**`SOURCE: RAW`** works from the sensor data instead. It takes minutes
rather than seconds, some colour adjustments can't be applied, and
`ACROS` won't be black and white.

`FILM SPEED 50` on the picker is only a label. It does not change your
camera's ISO.

Your raw files are never modified. Delete the JPEG and the photo is
exactly as the camera shot it.

<br>

### Film-in-ML (50D, 6D, 5D Mark III)

On the **Film** page:

| row | what it does |
|:--|:--|
| **Film** | off leaves every file alone. On develops each new raw. |
| **Delete CR2** | off keeps the raw. On deletes it only after `FLM_nnnn.JPG` exists. |
| **Stock** | the look. The wheel changes it. |

The choice is written to `ML/SE.CFG` and survives switching the camera off.

Take a photo. The screen shows `FILM ACROS 43,71%` until the JPEG is
finished. You can keep shooting while it works. When the box goes away,
open playback on that shot: with **Delete CR2** off, the raw's preview is
already the look. `FLM_1234.JPG` is the same picture as its own file.

<br>

> ### ⚠️ Set your Picture Style to Standard, Neutral or Faithful
>
> On Monochrome every look comes out black and white, because the camera
> hands this a grey picture to start from and there's no colour in it
> to work with.

<br>

The look is applied to the JPEG preview Canon already embedded in the
raw, not to the sensor data. That is why a monochrome picture style
comes out black and white: the preview arrives with no colour left.

<br>

---

<br>

## 🎞️ The films

Thirteen, still under development.

They're small text files in `ML/FILM` on the card, so you can read them,
change them, or write your own. The camera lists whatever it finds
there.

<br>

<div align="center">

### 🎨 [Soup Stocks](https://jiijii0.github.io/soup-stocks/)

**A web editor for the film stocks.**

Drop in a photo, move sliders, download a `.fs`, put it on the card.

The preview is this engine's own code compiled to WebAssembly, so it
matches what the camera writes.<br>Your photo never leaves your browser.

</div>

<br>

---

<br>

## 🧹 Removing it

<br>

### Classic (5D Classic, 40D)

Put Magic Lantern's original `autoexec.bin` back. That's all.

To pause it without uninstalling, delete `SE.BIN`. The camera boots
normally without it.

> 🆘 **If the camera ever misbehaves:** pull the battery, put the card
> in a computer, delete `SE.BIN`. Don't delete `AUTOEXEC.BIN` while the
> boot flag is on, because with the flag set and no `AUTOEXEC.BIN` the
> camera won't start at all.

<br>

### Film-in-ML (50D, 6D, 5D Mark III)

Put Magic Lantern's original `autoexec.bin` back, and put a matching
`ML/modules/<MODEL>_<FW>.sym` beside it. These bodies do not boot
`SE.BIN`; deleting that file does not uninstall the Film page.

> 🆘 **If the camera ever misbehaves:** pull the battery, put the card
> in a computer, restore stock Magic Lantern's `AUTOEXEC.BIN` and
> matching `.sym`. Don't delete `AUTOEXEC.BIN` while the boot flag is on.

<br>

---

<br>

## ❤️ Thanks

This wouldn't exist without [Magic Lantern](https://magiclantern.fm).

Soup Engine runs inside their work. Their builds are what let the cameras
run any of this, and years of their reverse engineering made it possible
to understand. They're worth supporting.

Soup Engine isn't their project, so please don't take problems with it
to them. Open an issue here instead.

<br>

## 📄 Source and licence

All of it is in [`src/`](src).

- **Classic:** `AUTOEXEC.BIN` is Magic Lantern with a small binary patch;
  `tools/patch-film.py` applies it. Platforms under
  `src/ml/platforms/5DC.111` and `40D.111`.
- **Film-in-ML:** `AUTOEXEC.BIN` is a rebuilt Magic Lantern with overlays
  from [`integrations/magiclantern/`](integrations/magiclantern/), built by
  `tools/build-ml.py`.

GPL v2. See [LICENSE](LICENSE). Distributed **without any warranty**,
including the implied warranties of merchantability and fitness for a
particular purpose (sections 11 and 12).
