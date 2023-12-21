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