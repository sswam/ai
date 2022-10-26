import os
import gradio as gr
import torch
import numpy as np
from transformers import pipeline

import torch
print(f"Is CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}")

pipe_flan = pipeline("text2text-generation", model="google/flan-t5-xxl", device="cuda:0", model_kwargs={"torch_dtype":torch.bfloat16})
pipe_vanilla = pipeline("text2text-generation", model="t5-large", device="cuda:0", model_kwargs={"torch_dtype":torch.bfloat16})

examples = [
  ["Please answer to the following question. Who is going to be the next Ballon d'or?"],
  ["Q: Can Barack Obama have a conversation with George Washington? Give the rationale before answering."],
  ["Summarize the following text: Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth collapsed and was rushed to the hospital. Since she was diagnosed with a brain injury, the doctor told Peter to stay besides her until she gets well. Therefore, Peter stayed with her at the hospital for 3 days without leaving."],
  ["Please answer the following question: What is the boiling point of water?"],
  ["Translate to German: How old are you?"],
  ["Answer the following yes/no question by reasoning step-by-step. Can you write a whole Haiku in a single tweet?"],
  ["Premise:  At my age you will probably have learnt one lesson. Hypothesis:  It's not certain how many lessons you'll learn by your thirties. Does the premise entail the hypothesis?"],
  ["Answer the following question by reasoning step by step. The cafeteria had 23 apples. If they used 20 for lunch and bought 6 more, how many apples do they have?"],
]

title = "Flan T5 and Vanilla T5"
description = "This demo compares [T5-large](https://huggingface.co/t5-large) and [Flan-T5-X-large](https://huggingface.co/google/flan-t5-xl). Note that T5 expects a very specific format of the prompts, so the examples below are not necessarily the best prompts to compare."

def inference(text):
  output_flan = pipe_flan(text, max_length=100)[0]["generated_text"]
  output_vanilla = pipe_vanilla(text, max_length=100)[0]["generated_text"]
  return [output_flan, output_vanilla]

io = gr.Interface(
  inference,
  gr.Textbox(lines=3),
  outputs=[
    gr.Textbox(lines=3, label="Flan T5"),
    gr.Textbox(lines=3, label="T5")
  ],
  title=title,
  description=description,
  examples=examples
)
io.launch()
