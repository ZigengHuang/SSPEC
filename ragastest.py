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