"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
import logging
import os
from typing import Union

import markdown
import pydot
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import from_pydot

from config import setup_logging


logger = setup_logging(__name__, log_level=logging.DEBUG)


def dot_to_digraph(dot_string: str) -> MultiDiGraph:
    """
    Convert a DOT string to a NetworkX MultiDiGraph.

    Args:
        dot_string: The DOT string representation of the graph.

    Returns:
        A NetworkX MultiDiGraph object.
    """
    pgraph: Union[pydot.Dot, pydot.Graph, pydot.Cluster] = pydot.graph_from_dot_data(dot_string)[0]
    return from_pydot(pgraph)


def convert_pdf_to_txt(pdf_path: str, txt_path: str) -> None:
    """Convert a PDF file to a text file"""
    logger.info(f"Converting {pdf_path} to {txt_path}.")
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ' '.join(page.extract_text() for page in pdf_reader.pages)
        text = ' '.join(text.splitlines())
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def convert_md_to_txt(md_path: str, txt_path: str) -> None:
    """Convert a Markdown file to a text file"""
    logger.info(f"Converting {md_path} to {txt_path}.")
    with open(md_path, encoding='utf-8') as md_file:
        md_content = md_file.read()
        html = markdown.markdown(md_content)
        text = ''.join(BeautifulSoup(html, features='html.parser').findAll(text=True))
        text = ' '.join(text.splitlines())
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def traverse_and_convert_all_to_txt(raw_dir: str, processed_dir: str) -> None:
    """
    Traverse and Convert Files to Text

    This function traverses through a given directory and converts all files with the extensions '.pdf' or '.md' to
    text format. The converted text files are saved in a specified directory.
    """
    for filename in os.listdir(raw_dir):
        name, ext = os.path.splitext(filename)

        if ext == '.pdf':
            pdf_path = os.path.join(raw_dir, filename)
            txt_path = os.path.join(processed_dir, f'{name}.txt')
            convert_pdf_to_txt(pdf_path, txt_path)
        elif ext == '.md':
            md_path = os.path.join(raw_dir, filename)
            txt_path = os.path.join(processed_dir, f'{name}.txt')
            convert_md_to_txt(md_path, txt_path)
