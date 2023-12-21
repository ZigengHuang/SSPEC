import openai
import pandas as pd
import os
import numpy as np
import ragastest
import in_eval
import get_response
import re_get_response
import risk_detection
from datasets import Dataset
from langchain.evaluation import load_evaluator
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness
)
os.environ["OPENAI_API_KEY"] = "key_value"


# Input question
question = input("Please enter your question.")
# System prompt (general)
prompt1  = pd.read_csv("general_prompt.csv")
# Assistant prompt(SSPEC)
prompt2  = pd.read_csv("SSPEC_prompt.csv")

# Generate response
answer = get_response(question,prompt1,prompt2)

# GPT evaluation
inscore = in_eval(question,answer)
# Ragas evaluation
ragasscore = ragastest(question,prompt1,prompt2,answer)
# Risk detection
riskscore = risk_detection(answer)

# Define the threshold to trigger reflection.
reflect = [inscore,ragasscore,riskscore]


# Reflection (maximum 3 times)
i = 1
while (reflect!=[1,1,1]):
    i=i+1
    if i>3: 
        print("warning message") 
        break
    answer = re_get_response(question,prompt1,prompt2,answer)
    inscore = in_eval(question,answer)
    ragasscore = ragastest(question,prompt1,prompt2,answer)
    riskscore = risk_detection(answer)

# Output final response
print(answer)