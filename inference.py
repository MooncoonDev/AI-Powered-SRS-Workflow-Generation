"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
import logging
from pathlib import Path

from networkx import MultiDiGraph

from config import setup_logging
from utils import dot_to_digraph


logger = setup_logging(__name__, log_level=logging.DEBUG)


def infer_dotfile(srs_document_path: Path | str) -> MultiDiGraph:
    srs: str = Path(srs_document_path).read_text()
    try:
        inferred_dot =
        inferred_digraph: MultiDiGraph = dot_to_digraph(inferred_dot)
    except Exception as e:
        logger.error(e)
        raise from e
    return inferred_digraph


def generate_visual_workflow_graph(digraph: MultiDiGraph) -> None:
    ...
