import torch
from transformers import BertTokenizer, BertForSequenceClassification
from django.conf import settings

MODEL_NAME = settings.HF_MODEL_NAME  

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

labels = settings.EMOTION_LABELS

def predict_emotion(text):
    """
    Prediksi emosi dari teks input.
    Returns dict dengan label, confidence, dan semua skor.
    """

    # Tokenisasi
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)[0]
        pred_idx = torch.argmax(probabilities).item()

    # Return hasil
    return {
        "emotion": labels[pred_idx],
        "confidence": float(probabilities[pred_idx]),
        "all_scores": {
            labels[i]: float(probabilities[i]) for i in range(len(labels))
        }
    }
