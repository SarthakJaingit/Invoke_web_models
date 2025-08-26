from transformers import pipeline
import torch

model_id = "Qwen/Qwen2.5-14B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype="auto",
    device_map="cuda:0",
)

# messages = [
#     {"role": "user", "content": "Explain quantum mechanics clearly and concisely."},
# ]

messages = [
    {"role": "user", "content": "What does VBO tickets sell"},
]

outputs = pipe(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])