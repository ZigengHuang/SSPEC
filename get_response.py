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