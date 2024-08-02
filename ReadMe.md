# IASS2024

This is a temporary repository for storing and testing files for the upcoming workshop at IASS2024.

```bash
conda create -n iass -c conda-forge compas compas_occ compas_viewer
```

```bash
cd code_directory
conda activate iass
git clone https://github.com/compas-dev/compas_viewer.git
cd compas_viewer && pip install -e . && ..
git clone https://github.com/compas-dev/compas_ifc.git
cd compas_ifc && pip install -e . && ..
git clone https://github.com/BlockResearchGroup/compas-FoFin
cd compas_fofin && pip install -e . && ..
```