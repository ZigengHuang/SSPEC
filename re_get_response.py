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