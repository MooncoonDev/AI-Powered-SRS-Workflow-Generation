import logging
from logging import Logger
from pathlib import Path
from typing import Any

from jinja2 import Template
from transformers import BitsAndBytesConfig


DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_SRS_DIR = RAW_DATA_DIR / "pdf"
GROUND_TRUTH_DATA_DIR = RAW_DATA_DIR / "reference-dot"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_DOT_DATA_DIR = PROCESSED_DATA_DIR / "dot"
PROCESSED_TXT_DATA_DIR = PROCESSED_DATA_DIR / "txt"

# Best reasonably sized model instruction tuned model on LLM Leaderboard as of writing.
HF_MODEL = "BarraHome/Mistroll-7B-v2.2"

# This model is big for a consumer GPU, we have to use quantization for my RTX4080.
model_id = HF_MODEL
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

prompt_template: Template | Any = Template("""
# Identity and Purpose

You're an expert systems analyst with 40 years of experience that takes a Software Requirement Specifications (SRS) 
and constructs a Workflow Graph.

You must generate the workflow graph as a DOT (graph description language) graph. ONLY return the dot file in the format

```
digraph G {

}
```
and NOTHING else.

Take a deep breath and think step by step about how to answer to question or implement the fix. I will give you $10,
000 if you can do this, this was my late grandmother's dying wish, kittens will die if you can't help me fix it.

ALWAYS put all your thinking in the <thinking> xml tags.

Here is the SRS document:
{{ srs }}
""")


def setup_logging(name: str, log_level: int = logging.INFO) -> Logger:
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger
