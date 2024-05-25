# AI-Powered SRS Workflow Generation

## Introduction

This project explores the use of language models to automate the construction of workflow graphs from
Software Requirement Specification (SRS) documents. The goal is to develop an AI system that can analyze textual
requirements in SRS documents and generate corresponding workflow graphs, facilitating the visualization and
understanding of complex software processes. To train and evaluate the system, a novel approach is used.

A strong language model, Claude Opus (claude-3-opus-20240229) is first used to generate "ground truth" workflow graphs
from a dataset of SRS documents. These generated graphs are then manually checked for accuracy, providing a labeled
dataset. The workflow graph generation pipeline then uses a weaker language model, allowing us to assess how
well the system can automate this task. Evaluation metrics such as
precision, recall, F1 score, and semantic similarity are used to quantify the system's effectiveness in capturing the
intended workflows described in the SRS documents.

A powerful Nvidia GPU is necessary for this to work within reasonable time frames.

## Dataset Description

The following datasets are all included in the pipeline and assigned a code for easy reference:

| Code | URL                                                                                                                                                                                                                 |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A    | https://github.com/mahmoudai1/school-management-system/blob/main/SRS.pdf                                                                                                                                            |
| B    | https://github.com/aliasar1/Hotel-Management-System-Documentation/blob/main/Software%20Design%20Specification%20(HMS).pdf                                                                                           |
| C    | https://github.com/vrinda41198/Digital-Bus-Automation-System/blob/main/Software%20Requirements%20Specification.pdf                                                                                                  |
| E    | https://github.com/munteanuic-zz/Voting-Aggregation-System/blob/main/WaterfallProject/SRS/SRS_Team5.pdf                                                                                                             |
| F    | https://github.com/MuhammadKazim01/Software-Requirement-and-Design-Specifications-for-Bank-Management-System/blob/main/Software%20Requirement%20and%20Design%20Specification%20for%20Bank%20Management%20System.pdf |

These are all publicly available SRS documents of varying quality. You can find out more about each project in the
accompanying repository.

Each file is stored in a synonymously named PDF or markdown file depending on the source, for example `A.pdf`, in
the `data` directory.
The processed text files will be saved to `data/processed/txt` and dot files to `data/processed/dot`. The manually (i.e.
Opus-AI-human assisted) labeled files is stored in `data/reference-dot` directory.

The ground truth samples are in DOT format; the task of the LLM will be to generate workflow graphs in dotfile format
too.

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

## Copyright

MIT licence

Copyright (c) 2024-Present Marcel Coetzee
