"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""

import os
import pydot
import subprocess
from PyPDF2 import PdfReader
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import from_pydot, write_dot
from pathlib import Path
from typing import Union

from srs_llm.config import setup_logging


logger = setup_logging(__name__)


def dot_to_digraph(dot_string: str) -> MultiDiGraph:
    """
    Convert a DOT string to a NetworkX MultiDiGraph.

    Args:
        dot_string: The DOT string representation of the graph.

    Returns:
        A NetworkX MultiDiGraph object.
    """
    pgraph: Union[pydot.Dot, pydot.Graph, pydot.Cluster] = (
        pydot.graph_from_dot_data(dot_string)[0]
    )
    return from_pydot(pgraph)


def convert_pdf_to_txt(pdf_path: str, txt_path: str) -> None:
    """Convert a PDF file to a text file"""
    logger.debug(f"Converting {pdf_path} to {txt_path}.")
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = " ".join(page.extract_text() for page in pdf_reader.pages)
        text = " ".join(text.splitlines())
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)


def convert_all_pdfs_to_txt(raw_dir: str, processed_dir: str) -> None:
    """
    Traverse and Convert Files to Text

    This function traverses through a given directory and converts all files with the extensions '.pdf' or '.md' to
    text format. The converted text files are saved in a specified directory.
    """
    for filename in os.listdir(raw_dir):
        name, ext = os.path.splitext(filename)

        if ext != ".pdf":
            raise ValueError(f"Only pdf file format supported: {filename}")

        pdf_path = os.path.join(raw_dir, filename)
        txt_path = os.path.join(processed_dir, f"{name}.txt")
        convert_pdf_to_txt(pdf_path, txt_path)


def generate_visual_workflow_graph(
        digraph: MultiDiGraph,
        dotfile_export_dir: Path | str,
        visual_export_dir: Path | str,
) -> None:
    """
    Exports the given DiGraph instance as a dotfile in `dotfile_export_dir`,
    and the accompanying PNG visual representation in `visual_export_dir`.
    """
    try:
        dotfile_path = Path(dotfile_export_dir)
        write_dot(digraph, dotfile_path)
        logger.debug(f"Exported dotfile to {dotfile_path}")

        visual_path = Path(visual_export_dir) / "workflow.png"
        subprocess.run(
            ["dot", "-Tpng", dotfile_path, "-o", visual_path], check=True
        )
        logger.debug(f"Exported PNG visual to {visual_path}")

    except Exception as e:
        logger.exception(f"Error generating visual workflow graph: {e}")
        raise
