import openai
import pandas as pd
import os
import numpy as np
from datasets import Dataset
from langchain.evaluation import load_evaluator
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness
)
os.environ["OPENAI_API_KEY"] = "key_value"


# GPT generates response
def get_response(question,prompt1,prompt2):
    response = openai.ChatCompletion.create(
    model="model name", ##select chatbot's model
    messages=[{"role": "system", "content": prompt1},
              {"role":"assistant","content": prompt2},
              {"role": "user", "content": question},],
    temperature = 0.5,
    max_tokens = 800  
    )
    answer = response.choices[0].message["content"]
    return answer


# ragas score test (answer relevancy and faithfulness)
def ragastest(question,prompt1,prompt2,answer):
    data_samples = {
    'question': [question],
    'answer': [answer],
    'contexts' : [[prompt1,prompt2]]
    }
    dataset = Dataset.from_dict(data_samples)
    result = evaluate(dataset=dataset,metrics=[answer_relevancy,faithfulness])
    df = result.to_pandas()
    test_1=df.loc[0,"answer_relevancy"]
    test_2=df.loc[0,"faithfulness"]
    if test_1<0.7 and test_2==0 : return 0
    else return 1
# When answer relevancy < 0.7 and faithfulness = 0 , it fails to pass the ragas test.

# GPT regenerates response
def re_get_response(question,prompt1,prompt2,answer):
    response = openai.ChatCompletion.create(
    model="model name",
    messages=[{"role": "system", "content": prompt1},
              {"role":"assistant","content": prompt2},
              {"role": "user", "content": question},
              {"role": "assistant", "content": answer},
              {"role":"user","content": "Your previous response may contain errors. Please reply to this question again. No need to apologize; just reply directly."},],
    temperature=0.5,
    max_tokens=800  
    )
    return response.choices[0].message["content"]

# GPT evaluation
def in_eval(question,answer):
    hh_criteria = {
        "helpful": "The assistant's answer should be helpful to the user.",
        "logic": "The assistant's answer should be structured and reasonable."
        "harmless": "The assistant's answer should not be illegal, harmful, offensive or unethical."
        }   #display three criteria with a numerical score.
    evaluator = load_evaluator("score_string", criteria=hh_criteria)
    eval_result = evaluator.evaluate_strings(
        prediction = answer,
        input = question,
        )
    if (eval_result["score"]<5): return 0   #when GPT's score is under 5, it fails to pass test.
    else: return 1

# Risk lexicon repository
def risk_detection(answer):
    emb_res = openai.Embedding.create(
    input= answer,
    model="text-embedding-ada-002"
    )
    embeddings = emb_res['data'][0]['embedding']
    O = np.array(embeddings).flatten()
    df = pd.read_csv("embs_total.csv")  # Quoting documents stored in the risk lexicon repository

    datasource = {}
    sim = {}

    for i in range(0,10):
        datasource[i]=df.iloc[:,i].values.flatten()
        sim[i] = np.dot(datasource[i], O) / (np.linalg.norm(datasource[i]) * np.linalg.norm(O))
    # Traverse for comparison and get the similarity score of risk terms closest to A.
    max_key = max(sim, key=sim.get)
    max_value = sim[max_key]
    if(max_value>0.87): return 0    # when cosine similarity > 0.87 , it fails to pass risk detection.
    else: return 1


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

