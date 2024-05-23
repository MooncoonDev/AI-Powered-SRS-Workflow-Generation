# AI Engineer Assessment

## Setup

First, install the miniforge package manager:

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

Then navigate to the project root and create the virtual environment with

```bash
mamba env create
```

And activate the newly created virtual environment with all necessary packages installed:

```bash
mamba activate srs-llm
```

## Running this project

Simple!

```
python main.py
```
