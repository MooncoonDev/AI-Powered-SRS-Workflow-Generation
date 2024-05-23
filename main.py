import pydot
from networkx.drawing import nx_pydot


def evaluate_workflow_graph(gt_graph, gen_graph):
    # Calculate metrics
    gt_nodes = set(gt_graph.nodes)
    gen_nodes = set(gen_graph.nodes)

    gt_edges = set(gt_graph.edges)
    gen_edges = set(gen_graph.edges)

    node_intersection = gt_nodes.intersection(gen_nodes)
    edge_intersection = gt_edges.intersection(gen_edges)

    # Calculate true positives, false positives, false negatives for nodes
    node_tp = len(node_intersection)
    node_fp = len(gen_nodes - gt_nodes)
    node_fn = len(gt_nodes - gen_nodes)

    # Calculate true positives, false positives, false negatives for edges
    edge_tp = len(edge_intersection)
    edge_fp = len(gen_edges - gt_edges)
    edge_fn = len(gt_edges - gen_edges)

    # Calculate precision, recall, F1 score for nodes
    node_precision = node_tp / (node_tp + node_fp) if (node_tp + node_fp) > 0 else 0
    node_recall = node_tp / (node_tp + node_fn) if (node_tp + node_fn) > 0 else 0
    node_f1 = 2 * (node_precision * node_recall) / (node_precision + node_recall) if (
                                                                                             node_precision +
                                                                                             node_recall) > 0 else 0

    # Calculate precision, recall, F1 score for edges
    edge_precision = edge_tp / (edge_tp + edge_fp) if (edge_tp + edge_fp) > 0 else 0
    edge_recall = edge_tp / (edge_tp + edge_fn) if (edge_tp + edge_fn) > 0 else 0
    edge_f1 = 2 * (edge_precision * edge_recall) / (edge_precision + edge_recall) if (
                                                                                             edge_precision +
                                                                                             edge_recall) > 0 else 0

    return {"node_precision": node_precision, "node_recall": node_recall, "node_f1": node_f1,
            "edge_precision": edge_precision, "edge_recall": edge_recall, "edge_f1": edge_f1}


if __name__ == "__main__":
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

    # Parse DOT strings directly to pydot graphs
    gt_pgraph = pydot.graph_from_dot_data(ground_truth_dot)[0]
    gen_pgraph = pydot.graph_from_dot_data(generated_dot)[0]

    # Convert pydot graphs to NetworkX graphs
    ground_truth_graph = nx_pydot.from_pydot(gt_pgraph)
    generated_graph = nx_pydot.from_pydot(gen_pgraph)

    # Evaluate the workflow graphs
    metrics = evaluate_workflow_graph(ground_truth_graph, generated_graph)
    print(metrics)

    assert (metrics["node_f1"] == 0.923076923076923)
