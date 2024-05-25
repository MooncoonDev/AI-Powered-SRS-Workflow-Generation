"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""

from pathlib import Path
from statistics import harmonic_mean
from typing import Dict

from networkx import MultiDiGraph
from transformers import pipeline

from srs_llm.config import HF_MODEL, prompt_template, setup_logging
from srs_llm.utils import dot_to_digraph


logger = setup_logging(__name__)


def generate_dot(srs: str) -> str:
    messages = [
        {"role": "user", "content": prompt_template.render(srs=srs).strip()}
    ]
    pipe = pipeline("text-generation", model=HF_MODEL, device="cuda")

    outputs = pipe(
        messages, max_new_tokens=800, do_sample=False, num_return_sequences=1
    )
    return outputs[0]["generated_text"]


def srs_file_to_dot(srs_document_path: Path | str) -> MultiDiGraph:
    logger.debug(f"Inferring dotfile from {srs_document_path}...")
    srs: str = Path(srs_document_path).read_text()

    try:
        inferred_dot = generate_dot(srs)
        inferred_digraph: MultiDiGraph = dot_to_digraph(inferred_dot)
    except Exception as e:
        logger.error(e)
        raise
    return inferred_digraph


def calculate_metrics(
        gt_graph: MultiDiGraph, gen_graph: MultiDiGraph
) -> Dict[str, float]:
    """
    Calculate the precision, recall, and F1-score metrics for node and edge predictions.

    Args:
        gt_graph: The ground truth graph.
        gen_graph: The generated graph.

    Returns:
        A dictionary containing the calculated metrics.
    """


    def precision(tp: int, fp: int) -> float:
        return tp / (tp + fp) if tp + fp > 0 else 0


    def recall(tp: int, fn: int) -> float:
        return tp / (tp + fn) if tp + fn > 0 else 0


    def f1_score(p: float, r: float) -> float:
        return harmonic_mean([p, r]) if p + r > 0 else 0

    gt_nodes, gt_edges = set(gt_graph.nodes), set(gt_graph.edges)
    gen_nodes, gen_edges = set(gen_graph.nodes), set(gen_graph.edges)

    node_intersection = gt_nodes.intersection(gen_nodes)
    edge_intersection = gt_edges.intersection(gen_edges)

    node_tp, edge_tp = len(node_intersection), len(edge_intersection)
    node_fp, edge_fp = len(gen_nodes - gt_nodes), len(gen_edges - gt_edges)
    node_fn, edge_fn = len(gt_nodes - gen_nodes), len(gt_edges - gen_edges)

    node_precision, edge_precision = precision(node_tp, node_fp), precision(
        edge_tp, edge_fp
    )
    node_recall, edge_recall = recall(node_tp, node_fn), recall(
        edge_tp, edge_fn
    )
    node_f1, edge_f1 = f1_score(node_precision, node_recall), f1_score(
        edge_precision, edge_recall
    )

    # We take the harmonic mean instead of raw tp + fp etc.
    # because we don't want the more numerous edges to potentially down out the nodes.
    overall_precision = harmonic_mean([node_precision, edge_precision])
    overall_recall = harmonic_mean([node_recall, edge_recall])
    overall_f1 = f1_score(overall_precision, overall_recall)

    return {
        "node_precision": node_precision,
        "node_recall": node_recall,
        "node_f1": node_f1,
        "edge_precision": edge_precision,
        "edge_recall": edge_recall,
        "edge_f1": edge_f1,
        "precision": overall_precision,
        "recall": overall_recall,
        "f1": overall_f1,
    }
