import json
import re
import hashlib, unicodedata

with open("firecrawl_ft_3_scrape_result.json", "r", encoding="utf-8") as f:
    results = json.load(f)

data = list()

def pretty_print_data(data):
    for i, d in enumerate(data):
        print(f"{i}.: Question: {d[0]} | Answer: {d[1]}")
        print("\n")


def preprocess_data(results):
    # print(results["data"]["markdown"])
    faqs = results["data"]["json"]["faqs"]
    print(f"{len(faqs)} number of FAQS")
    for data_point in faqs:
        original_question = data_point["question"]
        original_answer = data_point["answer"]
        data.append((original_question, original_answer))
    pretty_print_data(data)

def preprocess_data_with_paraphrased(results):
    # print(results["data"]["markdown"])
    faqs = results["data"]["json"]["faqs"]
    print(f"{len(faqs)} number of FAQS")
    for data_point in faqs:
        original_question = data_point["question"]
        original_answer = data_point["answer"]
        variants = data_point["variants"]
        for v in variants:
            variant_question = v["question"]
            variant_answer = v["answer"]
            data.append((variant_question, variant_answer))
        data.append((original_question, original_answer))
    pretty_print_data(data)
    
    



if __name__ == "__main__":
    preprocess_data(results)
    # preprocess_data_with_paraphrased(results)
    