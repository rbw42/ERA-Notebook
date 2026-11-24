import piplite

async def install():

    await piplite.install([
        # Pure-Python packages, fetched from PyPI at runtime.
        # Keep these in step with the versions pinned in requirements.txt,
        # since the matching JupyterLab extensions are bundled at build time.
        "ipywidgets==8.1.9",
        "plotly==7.1.0",
        "nbformat==5.11.1",           # needed by plotly to display figures in the notebook

        # Compiled packages provided by the Pyodide distribution (Pyodide 314.0.6).
        # Versions must match the Pyodide release bundled by jupyterlite-pyodide-kernel.
        "numpy==2.4.6",
        "astropy==7.2.0",
    ])
