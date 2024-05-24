"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
import logging
from statistics import harmonic_mean
from typing import Callable, Dict

from networkx import MultiDiGraph

from config import setup_logging, PROCESSED_TXT_DATA_DIR, RAW_SRS_DIR
from utils import dot_to_digraph, convert_all_pdfs_to_txt


logger = setup_logging(__name__, log_level=logging.DEBUG)


def calculate_metrics(gt_graph: MultiDiGraph, gen_graph: MultiDiGraph) -> Dict[str, float]:
    """
    Calculate the precision, recall, and F1-score metrics for node and edge predictions.

    Args:
        gt_graph: The ground truth graph.
        gen_graph: The generated graph.

    Returns:
        A dictionary containing the calculated metrics.
    """
    precision: Callable[[int, int], float] = lambda tp, fp: tp / (tp + fp) if (tp + fp) > 0 else 0
    recall: Callable[[int, int], float] = lambda tp, fn: tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score: Callable[[float, float], float] = lambda p, r: harmonic_mean([p, r]) if (p + r) > 0 else 0

    gt_nodes, gt_edges = set(gt_graph.nodes), set(gt_graph.edges)
    gen_nodes, gen_edges = set(gen_graph.nodes), set(gen_graph.edges)

    node_intersection = gt_nodes.intersection(gen_nodes)
    edge_intersection = gt_edges.intersection(gen_edges)

    node_tp, edge_tp = len(node_intersection), len(edge_intersection)
    node_fp, edge_fp = len(gen_nodes - gt_nodes), len(gen_edges - gt_edges)
    node_fn, edge_fn = len(gt_nodes - gen_nodes), len(gt_edges - gen_edges)

    node_precision, edge_precision = precision(node_tp, node_fp), precision(edge_tp, edge_fp)
    node_recall, edge_recall = recall(node_tp, node_fn), recall(edge_tp, edge_fn)
    node_f1, edge_f1 = f1_score(node_precision, node_recall), f1_score(edge_precision, edge_recall)

    # We take the harmonic mean instead of raw tp + fp etc.
    # because we don't want the more numerous edges to potentially down out the nodes.
    overall_precision = harmonic_mean([node_precision, edge_precision])
    overall_recall = harmonic_mean([node_recall, edge_recall])
    overall_f1 = f1_score(overall_precision, overall_recall)

    return {"node_precision": node_precision, "node_recall": node_recall, "node_f1": node_f1,
            "edge_precision": edge_precision, "edge_recall": edge_recall, "edge_f1": edge_f1,
            "precision": overall_precision, "recall": overall_recall, "f1": overall_f1}


if __name__ == "__main__":
    # Data preprocessing.
    convert_all_pdfs_to_txt(RAW_SRS_DIR, PROCESSED_TXT_DATA_DIR)
    # infer_dotfiles(RAW_DATA_DIR, PROCESSED_TXT_DATA_DIR)

    ground_truth_dot = """
    digraph workflow {
      Start -> "Task 1" -> "Task 2";
      "Task 2" -> "Task 3";
      "Task 2" -> "Task 4";
      "Task 3" -> End;
      "Task 4" -> End;
    }
    """

    generated_dot = """
    digraph workflow {
      Start -> "Task 1" -> "Task 2";
      "Task 2" -> "Task 3";
      "Task 2" -> "Task 4";
      "Task 3" -> "Task 5" -> End;
      "Task 4" -> End;
    }
    """

    ground_truth_graph, generated_graph = dot_to_digraph(ground_truth_dot), dot_to_digraph(generated_dot)
    metrics = calculate_metrics(ground_truth_graph, generated_graph)

    logger.warning(metrics)
