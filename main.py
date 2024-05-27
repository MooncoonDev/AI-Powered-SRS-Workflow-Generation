"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
from pathlib import Path

from networkx import MultiDiGraph

from srs_llm.config import PROCESSED_TXT_DATA_DIR, RAW_SRS_DIR, setup_logging, PROCESSED_DOT_DATA_DIR, \
    VISUAL_REPRESENTATIONS_DATA_DIR
from srs_llm.inference import srs_file_to_dot, get_llm_pipe
from srs_llm.utils import convert_all_pdfs_to_txt, generate_visual_workflow_graph


logger = setup_logging(__name__)


def main() -> None:
    # Data preprocessing.
    convert_all_pdfs_to_txt(RAW_SRS_DIR, PROCESSED_TXT_DATA_DIR)

    # Infer each file to dotfile and get accompanying visual representation.
    pipe = get_llm_pipe()
    for srs_file in PROCESSED_TXT_DATA_DIR.iterdir():
        dot: MultiDiGraph | None = srs_file_to_dot(srs_file, pipe)
        if not dot:
            continue
        file_name = srs_file.stem
        dotfile_file_path: Path = PROCESSED_DOT_DATA_DIR / f"{file_name}.dot"
        png_file_path: Path = VISUAL_REPRESENTATIONS_DATA_DIR / f"{file_name}.png"
        generate_visual_workflow_graph(dot, dotfile_file_path, png_file_path)

    # ground_truth_graph, generated_graph = dot_to_digraph(ground_truth_dot), dot_to_digraph(generated_dot)  #  #  #
    # metrics = calculate_metrics(ground_truth_graph, generated_graph)  # logger.warning(metrics)


if __name__ == "__main__":
    main()
