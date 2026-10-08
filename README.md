# Gorkhali Danab · गोर्खाली दानव

<p align="center">
  <img src="logo/gorkhali-danab-logo.svg" alt="Gorkhali Danab logo" width="420">
</p>

## The logo

The mark is a fierce *danab* (दानव, demon) built entirely from symbols of Nepal:

| Element | Meaning |
| --- | --- |
| **Lakhey mask face** | The red, fanged, wild-maned demon of Newar festivals in Kathmandu valley: a protector, not a villain |
| **Himalayan crown** | Snow-capped peaks with Sagarmatha (Everest) at the centre, lit from the upper left |
| **Crescent horns** | Together the horns form an upturned crescent, echoing the moon on the flag |
| **Moon on the crown band** | The flag's rayed moon, set on the flag's border blue |
| **Third eye** | The flag's twelve-rayed white sun, placed directly below the moon as on the flag |
| **Crossed khukuris** | The blade of the Gorkhali (Gurkha) soldier, crossed as on the regimental badge |
| **Crimson and blue** | Nepal's national colours: crimson for the rhododendron and courage, blue for peace |
| **Devanagari name** | गोर्खाली दानव, so the name reads in Nepali as well as in English |

## Files

| File | Use |
| --- | --- |
| `logo/gorkhali-danab-logo.svg` | Primary vertical logo on light backgrounds |
| `logo/gorkhali-danab-logo-dark.svg` | Primary vertical logo on navy |
| `logo/gorkhali-danab-horizontal.svg` | Wide layout for headers, banners, jerseys |
| `logo/gorkhali-danab-horizontal-dark.svg` | Wide layout on navy |
| `logo/gorkhali-danab-emblem.svg` | Emblem only, for avatars, favicons, stickers, patches |
| `logo/png/` | PNG exports: emblem at 32 to 2048 px, logos at 1x and 2x |

All text is converted to outlines, so the SVGs render identically everywhere without installing fonts.

## Colours

| Swatch | Hex | Role |
| --- | --- | --- |
| Crimson | `#DC143C` | Nepal flag crimson: face, *DANAB* |
| Flag blue | `#003893` | Nepal flag border: badge, crown band, Devanagari |
| Night navy | `#0A1A3F` | Outlines, *GORKHALI*, dark backgrounds |
| Marigold gold | `#FFC233` | Crown, horns, badge ring |
| Snow white | `#FFFFFF` | Sun, moon, snow caps, fangs |

## Typography

- **Cinzel Black**: *GORKHALI DANAB*
- **Eczar ExtraBold**: गोर्खाली दानव

Both typefaces are free under the SIL Open Font License.

## Editing the logo

The artwork is generated from code in `logo/src/`, so you can change shapes, colours or proportions and rebuild every file at once:

```bash
pip install fonttools uharfbuzz
npm install playwright          # or point NODE_PATH at a global install
logo/src/build.sh               # downloads the fonts on first run
```

`emblem.py` draws the emblem, and `lockup.py` sets the wordmark and writes all five SVGs. `build.sh` then exports the PNGs.
