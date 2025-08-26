import pandas as pd
from sentence_transformers import CrossEncoder
import torch
import time
import numpy as np
from tqdm import tqdm

# Models to try:
# Try Cohere ReRank v3
#(High Recall, Slow)
# bge-large-en-v1.5 
# intfloat/e5-large-v2 

# (Decent Recall, Fast)
# bge-base-en-v1.5
# intfloat/e5-base-v2

# (Decent Precision but Faster)
# BAAI/bge-reranker-base

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model_name = "BAAI/bge-reranker-large"
model_name = "BAAI/bge-reranker-base"
print(model_name)
model = CrossEncoder(model_name, device=device, max_length=512)
batch_size = 100

def match_local(business_shopify_pth, query):
    # Get the best result
    topk = 1
    df = pd.read_csv(business_shopify_pth)
    text_col = df.columns[0]               
    texts = df[text_col].astype(str).fillna("")

    pairs = [(query, t) for t in texts]
    scores = model.predict(pairs, batch_size=batch_size) 
    order = np.argsort(scores)[::-1][:topk][0]
    return order

def run_eval_gt_av(func, eval_db_pth, business_shopify_pth):
    df = pd.read_csv(eval_db_pth)
    hits = 0
    for i in tqdm(range(len(df))):
        query, gt_index = df.iloc[i, 0], df.iloc[i, 1]
        pred = match_local(business_shopify_pth, query)
        hits += (pred == gt_index)
        if (pred != gt_index):
            print(f"{query} | GT: {gt_index} | ")

    
    accuracy = hits / len(df)
    print("Accuracy: {}".format(accuracy))

def run_full_eval(func, eval_db_pth, business_shopify_pth):
    run_eval_gt_av(func, eval_db_pth, business_shopify_pth)


if __name__ == "__main__":
    business_shopify_pth = "shopify_100_unique_flows.csv"
    query = "Can I see how well my stuff does financially"
    start_time = time.time()
    eval_db_pth = "shopify_reranker_eval_queries.csv"
    run_eval_gt_av(match_local, eval_db_pth, business_shopify_pth)
    # match_local(business_shopify_pth, query)
    print("Latency: {}".format(time.time() - start_time))

