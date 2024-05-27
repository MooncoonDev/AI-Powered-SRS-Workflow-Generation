"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""

from pathlib import Path
from statistics import harmonic_mean
from typing import Any, Dict, Optional

from networkx import MultiDiGraph
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Pipeline,
    PreTrainedModel,
    PreTrainedTokenizerFast,
    TFPreTrainedModel,
    pipeline,
)

from srs_llm.config import (
    HF_MODEL,
    extract_workflow_text,
    prompt_template,
    setup_logging,
    system_prompt,
)
from srs_llm.utils import dot_to_digraph

logger = setup_logging(__name__)


def get_llm_pipe(model_id: str = HF_MODEL) -> Pipeline:
    model: str | PreTrainedModel | TFPreTrainedModel | None = (
        AutoModelForCausalLM.from_pretrained(model_id)
    )
    tokenizer: PreTrainedTokenizerFast | Any = AutoTokenizer.from_pretrained(
        model_id
    )
    return pipeline(
        "text-generation", model=model, tokenizer=tokenizer, device="cuda"
    )


def generate_dot(srs: str, llm_pipe: Pipeline) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_template.render(srs=srs).strip()},
    ]
    outputs = llm_pipe(
        messages, max_new_tokens=1000, do_sample=False, num_return_sequences=1
    )
    assistant_answer = outputs[0]["generated_text"][-1]["content"]

    return extract_workflow_text(assistant_answer).strip()


def srs_file_to_dot(
    srs_document_path: Path | str, llm_pipe: Pipeline
) -> Optional[MultiDiGraph]:
    logger.debug(f"Inferring dotfile from {srs_document_path}...")
    srs: str = Path(srs_document_path).read_text()

    inferred_dot = generate_dot(srs, llm_pipe=llm_pipe)
    logger.debug(f"Model generated the following dotfile:\n{inferred_dot}")
    try:
        inferred_digraph: Optional[MultiDiGraph] = dot_to_digraph(inferred_dot)
        return inferred_digraph
    except TypeError:
        logger.warning(
            f"The inferred dotfile for SRS document {srs_document_path.stem}"
            f" is malformed! Skipping {srs_document_path.stem}..."
        )
        return
    except:
        raise


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
    # because we don't want the more numerous edges to potentially drown out the nodes.
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
