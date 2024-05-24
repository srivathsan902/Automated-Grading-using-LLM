from generate_prompt import get_prompt
from get_grade import get_grade
from generate_report import create_pdf
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from tqdm import tqdm


from langchain.prompts import PromptTemplate