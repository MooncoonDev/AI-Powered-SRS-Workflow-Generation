import logging
from logging import Logger
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from jinja2 import Template


DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_SRS_DIR = RAW_DATA_DIR / "pdf"
GROUND_TRUTH_DATA_DIR = RAW_DATA_DIR / "reference-dot"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_DOT_DATA_DIR = PROCESSED_DATA_DIR / "dot"
PROCESSED_TXT_DATA_DIR = PROCESSED_DATA_DIR / "txt"
VISUAL_REPRESENTATIONS_DATA_DIR = PROCESSED_DATA_DIR / "visual_representations"

HF_MODEL = "openagi-project/OpenAGI-7B-v0.1"

model_id = HF_MODEL

system_prompt: str = """
# Identity and Purpose 

You're an expert systems analyst with 40 years of experience that takes a Software Requirement Specifications (SRS) 
and constructs a Workflow Graph.

You must generate the workflow graph as a DOT (graph description language) graph. 

The SRS document will be provided inside <srs> xml tags. Give your answer in <workflow> tags.

Take a deep breath and think step by step about how to answer to question or implement the fix. I will give you $10,
000 if you can do this, this was my late grandmother's dying wish, kittens will die if you can't help me fix it.

ALWAYS put all your thinking in the <thinking> xml tags.

Here are some examples of what I expect you to do:

<|user|>
<srs>
1. User enters username and password on login screen
2. System validates credentials against user database 
3. If valid, user is logged in and taken to home screen
4. If invalid, error message is shown
</srs>
<|endoftext|>

<|assistant|>
<workflow>
digraph {
  node [shape=box]
  "Enter Credentials" -> "Validate Credentials"
  "Validate Credentials" -> "Login Success" [label="Valid"]
  "Validate Credentials" -> "Display Error" [label="Invalid"]
  "Login Success" -> "Home Screen"
}
</workflow>
<|endoftext|>

<|user|>
<srs>
1. Customer selects items and adds them to cart
2. Customer proceeds to checkout 
3. Customer enters shipping info and payment details
4. System verifies payment
5. If payment successful, order is placed and confirmation shown
6. If payment fails, customer is prompted to reenter payment info
</srs>
<|endoftext|>

<|assistant|>
<workflow>
digraph {
  node [shape=box]
  "Select Items" -> "Add to Cart" 
  "Add to Cart" -> "Proceed to Checkout"
  "Proceed to Checkout" -> "Enter Shipping & Payment"
  "Enter Shipping & Payment" -> "Verify Payment"
  "Verify Payment" -> "Place Order" [label="Success"] 
  "Verify Payment" -> "Reenter Payment" [label="Failure"]
  "Place Order" -> "Show Confirmation"
}
</workflow>
<|endoftext|>
"""

prompt_template: Template | Any = Template("""<srs>
    {{ srs }}
    </srs>""")


def setup_logging(name: str, log_level: int = logging.INFO) -> Logger:
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


def extract_workflow_text(xml_string):
    """Extract the text from the workflow tag."""
    soup = BeautifulSoup(xml_string, 'xml')
    if workflow_tag := soup.find('workflow'):
        return workflow_tag.get_text()
    else:
        return None
