"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
import logging
from pathlib import Path

from networkx import MultiDiGraph
from transformers import pipeline

from config import setup_logging, HF_MODEL, prompt_template
from utils import dot_to_digraph


logger = setup_logging(__name__, log_level=logging.DEBUG)


def generate_dot(srs: str) -> str:
    messages = [{"role": "user", "content": prompt_template.render(srs=srs).strip()}]
    pipe = pipeline("text-generation", model=HF_MODEL)

    # We try to make experiment repeatable and deterministic as possible.
    outputs = pipe(messages, max_new_tokens=800, do_sample=False, temperature=0.0, num_return_sequences=1)
    return outputs[0]["generated_text"]


def srs_file_to_dot(srs_document_path: Path | str) -> MultiDiGraph:
    logger.info(f"Inferring dotfile from {srs_document_path}...")
    srs: str = Path(srs_document_path).read_text()

    try:
        inferred_dot = generate_dot(srs)
        inferred_digraph: MultiDiGraph = dot_to_digraph(inferred_dot)
    except Exception as e:
        logger.error(e)
        raise
    return inferred_digraph
