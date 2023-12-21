import openai
openai.api_key = "api_key" #Your api key
input_0 = input("")

response = openai.Embedding.create(
    input = input_0,
    model = "text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']

print(embeddings)

