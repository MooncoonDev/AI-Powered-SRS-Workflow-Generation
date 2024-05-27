"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""

from pathlib import Path

import networkx as nx
from networkx import MultiDiGraph

from srs_llm.config import (
    GROUND_TRUTH_DATA_DIR,
    PROCESSED_DOT_DATA_DIR,
    PROCESSED_TXT_DATA_DIR,
    RAW_SRS_DIR,
    VISUAL_REPRESENTATIONS_DATA_DIR,
    setup_logging,
)
from srs_llm.inference import calculate_metrics, get_llm_pipe, srs_file_to_dot
from srs_llm.utils import (
    convert_all_pdfs_to_txt,
    generate_visual_workflow_graph,
)

logger = setup_logging(__name__)


def main() -> None:
    # Data preprocessing.
    convert_all_pdfs_to_txt(RAW_SRS_DIR, PROCESSED_TXT_DATA_DIR)

    # Infer each file to dotfile and get accompanying visual representation and metrics.
    pipe = get_llm_pipe()
    for srs_file in PROCESSED_TXT_DATA_DIR.iterdir():
        generated_dot: MultiDiGraph | None = srs_file_to_dot(srs_file, pipe)
        if not generated_dot:
            continue

        file_name = srs_file.stem
        dotfile_file_path: Path = (
            PROCESSED_DOT_DATA_DIR / file_name
        ).with_suffix(".dot")
        ground_truth_dot_file_path: str = (
            GROUND_TRUTH_DATA_DIR / file_name
        ).with_suffix(".dot")
        png_file_path: Path = (
            VISUAL_REPRESENTATIONS_DATA_DIR / file_name
        ).with_suffix(".png")

        generate_visual_workflow_graph(
            generated_dot, dotfile_file_path, png_file_path
        )

        logger.debug(f"Generating metrics report for SRS {file_name}...")
        ground_truth_dot: MultiDiGraph = nx.drawing.nx_pydot.read_dot(
            ground_truth_dot_file_path
        )
        report = calculate_metrics(ground_truth_dot, generated_dot)
        logger.info(report)


if __name__ == "__main__":
    main()
