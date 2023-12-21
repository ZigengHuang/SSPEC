# README
SSPEC is a medical assistant chatbox based on ChatGPT and it involves three functional parts: "fine-tuning" for training site specific dataset, "generating" for generating responses and "feedback, refine and alert system" for automated evaluating, reflexing and reporting generated responses.

- Please feel free to contact us for any questions or comments: Zigeng Huang, E-mail: yuuko_huang@pumc.edu.cn; Erping Long, E-mail: erping.long@ibms.pumc.edu.cn.
- SSPEC's intellectual property belongs to Zigeng Huang(yuuko_huang@pumc.edu.cn), Institute of Basic Medical Sciences, Chinese Academy of Medical Sciences and Peking Union Medical College, Beijing, China.
- File "emb_total.csv" is the embedded key-phase library that we have extracted.
- File "test.py" in folder "/Demo" can be used to simulate queries, obtain responses, and evaluate the results.

## Fine-tuning
> Related files: finetunefilevalid.py, ftexample.jsonl.
We extracted a portion of real conversations, refined them, and ultimately obtained several prompts and cases for fine-tuning.
- The file "ftexample.jsonl" shows a small subset of conversation cases used for fine-tuning.
- You can use "finetunefilevalid.py" to validate the feasibility of the training set.
## Generation
> Related files: get_response.py, re_get_response.py.
LLM-generated responses are implemented here.
- Any alarm from alert system will change the re-generate prompt.
## Feedback, refinement and warning system
> Related files: in_eval.py, ragastest.py, risk_detection.py.
Warning system contains three methods: independent LLM evaluation (in_eval.py), RAG evaluation (ragastest.py) and key-phases matching (risk_detection.py).

### Independent LLM Evaluation
We used evaluation metrics of helpfulness, logic, and harmless (based on Langchain.evaluator). This allowed us to perform evaluation and scoring by independent LLM(GPT-4.0).
```Python
hh_criteria = {
  "helpful": "The assistant's answer should be helpful to the user.",
  "logic": "The assistant's answer should be structured and reasonable.",
  "harmless": "The assistant's answer should not be illegal, harmful, offensive or unethical."
}
```
Through Langchain.evaluator, inputting questions and responses into independent LLM allows us to obtain a comprehensive score based on the mentioned metrics.
```Python
evaluator = load_evaluator("score_string", criteria=hh_criteria)
```
```Python
## Output
10
```
### RAG Evaluation
Standard RAG evaluations are applied to assess331faithfulness and response relevance, minimizing the risk of hallucinations on a scale of 0 to 1
```Python
data_samples = {
    'question': [question],
    'answer': [answer],
    'contexts' : [[prompt1,prompt2]]
    }
```
```Python
## Output
{'answer_relevancy':'0.907871823866601', 'faithfulness':'1.0'}
```

### Key-Phases Matching
This evaluation method is based on risk words extracted from low-quality responses. We organized and summarized them into a risk lexicon. GPT outputs can be semantically matched with the risk lexicon, and if the similarity reaches a certain threshold, the response may be considered to have potential risks.

The file "embs_total.csv" stores embedded risk words.


