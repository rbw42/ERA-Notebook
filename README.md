# ERA Notebook

A standalone web-based environment for the ERA (Educational Radio Array) school incursions.

It is a [JupyterLite](https://jupyterlite.readthedocs.io) site: Jupyter running entirely in the
browser using [Pyodide](https://pyodide.org) (Python compiled to WebAssembly). No server or
local Python install is needed by students.

Live site: https://icrar.github.io/ERA-Notebook/

## What is in the repo

| Path | Purpose |
|---|---|
| `content/Lesson-01.ipynb` | The lesson notebook |
| `content/ERA_lib/software/ERA.py` | Reads a uvfits file and makes the figures (uv coverage, visibilities, images) |
| `content/ERA_lib/software/DataDownloader.py` | Widget to download ERA observations from the data bucket |
| `content/ERA_lib/software/FileUploader.py` | Widget to upload your own uvfits file |
| `content/ERA_lib/requirements/dependencies.py` | Python packages installed **in the browser** when the notebook starts |
| `content/data/` | Logo and example uvfits files |
| `requirements.txt` | Python packages needed to **build** the site |
| `repl/jupyter-lite.json` | Settings for the REPL app |
| `.github/workflows/deploy.yml` | Builds the site and deploys it to GitHub Pages on every push to `main` |

Everything under `content/` is copied into the site and is visible in the JupyterLite file browser.

## Building and previewing locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp README.md content
.venv/bin/jupyter lite build --contents content --output-dir dist
.venv/bin/python -m http.server 8000 --directory dist
```

Then open http://localhost:8000/lab/index.html?path=Lesson-01.ipynb

Notes:
- Use a normal browser window. JupyterLite uses a service worker to make the `content/` files
  (including `ERA_lib`) visible to Python; private/incognito windows may block it.
- Students' browsers load Pyodide and its packages from the jsDelivr CDN, and ipywidgets/plotly
  from PyPI, so the site needs internet access.
- `dist/` and `.jupyterlite.doit.db` are build outputs and are git-ignored.

## Data

The **Download Data** widget fetches ERA observations from a Cloudflare R2 bucket
(`DataDownloader.base_url`). Files are named `<unix time>_<bpcal|fullcal>.uvfits` in a folder per
day, at 5 minute intervals.

The bucket only allows cross-origin requests from `https://icrar.github.io`, so downloads will
fail from a local build or a fork. Use the bundled example files in `content/data/` or the
upload widget when testing locally.

### Using your own data

Run the **Or upload your own data** cell and select a `.uvfits` file, then run the
"Using your own file?" cell to load it. The uploader has been tested with files up to 200 MB.

`ERA.DataFile` expects a single-source uvfits file with `FREQ`, `STOKES`, `RA` and `DEC` axes
and an `AIPS AN` antenna table. It has been tested with ERA data (50 antennas) and with
EDA2 / SKA-Low station data (256 antennas, 16 channels).

## Updating dependencies

There are two sets of dependencies, and they must agree:

1. `requirements.txt` pins the build tools. The `jupyterlite-pyodide-kernel` version decides
   which Pyodide release (and therefore which Python version) runs in the browser.
2. `content/ERA_lib/requirements/dependencies.py` lists what is installed in the browser.
   - Compiled packages (numpy, astropy) come from the Pyodide distribution, so their versions
     must match that Pyodide release's package list
     (`https://cdn.jsdelivr.net/pyodide/v<version>/full/pyodide-lock.json`).
   - Pure-Python packages (ipywidgets, plotly) come from PyPI and should match the versions in
     `requirements.txt`, because the matching JupyterLab extensions are bundled at build time.
   - `nbformat` is needed by plotly to display figures.

Packages with compiled code that are not part of Pyodide (for example `pyuvdata`) cannot be used.

## Adding a lesson

Add a new notebook to `content/`, set its kernel to **Python (Pyodide)**, start it with the same
setup cell as `Lesson-01.ipynb`, and clear all outputs before committing.
