import torch
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    text = text[:512]
    result = sentiment_analyzer(text)[0]
    label = result['label']
    score = result['score']
    return score if label == 'POSITIVE' else -score