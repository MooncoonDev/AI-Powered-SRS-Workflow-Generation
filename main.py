"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""

from srs_llm.config import PROCESSED_TXT_DATA_DIR, RAW_SRS_DIR, setup_logging
from srs_llm.inference import srs_file_to_dot
from srs_llm.utils import convert_all_pdfs_to_txt

logger = setup_logging(__name__)


def main() -> None:
    # Data preprocessing.
    convert_all_pdfs_to_txt(RAW_SRS_DIR, PROCESSED_TXT_DATA_DIR)

    # Infer each file to dotfile.
    for srs_file in PROCESSED_TXT_DATA_DIR.iterdir():
        dot = srs_file_to_dot(srs_file)
        logger.info(f"{srs_file}:\n{dot}\n")

    # ground_truth_graph, generated_graph = dot_to_digraph(ground_truth_dot), dot_to_digraph(generated_dot)  #  #  #
    # metrics = calculate_metrics(ground_truth_graph, generated_graph)  # logger.warning(metrics)


if __name__ == "__main__":
    main()
