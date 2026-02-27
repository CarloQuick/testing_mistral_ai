import pandas as pd
hg_path = 'hf://datasets/HuggingFaceH4/ultrachat_200k/data/test_gen-00000-of-00001-3d4cd8309148a71f.parquet'
df = pd.read_parquet(hg_path, engine='pyarrow')

# hf://datasets/HuggingFaceH4/ultrachat_200k/data/test_gen-00000-of-00001-3d4cd8309148a71f.parquet

df_train = df.sample(frac=0.995, random_state=200)
df_eval = df.drop(df_train.index)

df_train.to_json('data/ultrachat_chunk_train.jsonl', orient="records", lines=True)
df_eval.to_json('data/ultrachat_chunk_eval.jsonl', orient="records", lines=True)
