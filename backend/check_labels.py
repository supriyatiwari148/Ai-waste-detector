"""Run this to see the model's REAL label list before trusting any mapping:
    python check_labels.py
"""
import os
from dotenv import load_dotenv
load_dotenv()
from transformers import AutoConfig

model_id = os.getenv("MODEL_ID", "prithivMLmods/Trash-Net")
print("Model:", model_id)
print("Labels:", AutoConfig.from_pretrained(model_id).id2label)
