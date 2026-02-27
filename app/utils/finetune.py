import pandas as pd
from reformat_data import reformat_jsonl
from mistralai import Mistral
import os
from dotenv import load_dotenv
import json

hg_path = 'hf://datasets/HuggingFaceH4/ultrachat_200k/data/test_gen-00000-of-00001-3d4cd8309148a71f.parquet'
train_path = 'data/ultrachat_chunk_train.jsonl'
eval_path = 'data/ultrachat_chunk_eval.jsonl'

def create_json_data():
    # hg_path = 'hf://datasets/HuggingFaceH4/ultrachat_200k/data/test_gen-00000-of-00001-3d4cd8309148a71f.parquet'
    df = pd.read_parquet(hg_path, engine='pyarrow')

    # hf://datasets/HuggingFaceH4/ultrachat_200k/data/test_gen-00000-of-00001-3d4cd8309148a71f.parquet

    df_train = df.sample(frac=0.995, random_state=200)
    df_eval = df.drop(df_train.index)


    df_train.to_json(train_path, orient="records", lines=True)
    df_eval.to_json(eval_path, orient="records", lines=True)

    reformat_jsonl(train_path)
    reformat_jsonl(eval_path)

def upload_json():
    load_dotenv()
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    ultrachat_chunk_train = client.files.upload(file={
        "file_name": "ultrachat_chunk_train.jsonl",
        "content": open(train_path, "rb"),
    })
    ultrachat_chunk_eval = client.files.upload(file={
        "file_name": "ultrachat_chunk_eval.jsonl",
        "content": open(eval_path, "rb"),
    })

    fine_tune(ultrachat_chunk_train, ultrachat_chunk_eval)


def fine_tune(ultrachat_chunk_train, ultrachat_chunk_eval):
    load_dotenv()
    model: str = "ministral-8b-2512"
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)
    created_jobs = client.fine_tuning.jobs.create(
        model=model,
        hyperparameters={"training_steps": 10, "learning_rate":0.0001},
        training_files=[{"file_id": ultrachat_chunk_train.id, "weight": 1}],
        validation_files=[ultrachat_chunk_eval.id],
        auto_start=True
    )
    created_jobs

