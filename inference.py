"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
import logging
from pathlib import Path

from networkx import MultiDiGraph
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import setup_logging
from utils import dot_to_digraph


logger = setup_logging(__name__, log_level=logging.DEBUG)


def infer_dotfile(srs_document_path: Path | str) -> MultiDiGraph:
    srs: str = Path(srs_document_path).read_text()
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    try:
        inferred_dot = pipeline =
        inferred_digraph: MultiDiGraph = dot_to_digraph(inferred_dot)
    except Exception as e:
        logger.error(e)
        raise from e
    return inferred_digraph

