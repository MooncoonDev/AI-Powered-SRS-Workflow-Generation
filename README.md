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

## Corpus

The following datasets

- https://github.com/mahmoudai1/school-management-system/blob/main/SRS.pdf
- https://github.com/aliasar1/Hotel-Management-System-Documentation/blob/main/Software%20Requirements%20Specification%20(HMS)%20.pdf
- https://github.com/vrinda41198/Digital-Bus-Automation-System/blob/main/Software%20Requirements%20Specification.pdf
- https://github.com/Gr0ki/book-catalog/blob/main/documentation/Software_Requirements_Specification.md
- https://github.com/munteanuic-zz/Voting-Aggregation-System/blob/main/WaterfallProject/SRS/SRS_Team5.pdf
- https://github.com/MuhammadKazim01/Software-Requirement-and-Design-Specifications-for-Bank-Management-System/blob/main/Software%20Requirement%20and%20Design%20Specification%20for%20Bank%20Management%20System.pdf
- https://github.com/imprld01/Exchange/blob/master/%E8%BB%9F%E9%AB%94%E5%B7%A5%E7%A8%8B%E6%96%87%E4%BB%B6/%E8%BB%9F%E9%AB%94%E9%96%8B%E7%99%BC%E6%96%87%E4%BB%B6%E8%A6%8F%E7%AF%84-SRS-Exchange20170115.pdf

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

This work is under the MIT license.

Copyright (c) 2024-Present Marcel Coetzee
