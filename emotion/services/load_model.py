# emotion/services/load_model.py
import requests
import os
from django.conf import settings

# Ambil konfigurasi dari settings
MODEL_NAME = settings.HF_MODEL_NAME  # "hasanfadh/indo-bert-emosense"
labels = settings.EMOTION_LABELS  # ["Senang", "Marah", "Sedih", "Takut", "Netral"]

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"


def predict_emotion(text):
    """
    Prediksi emosi dari teks input menggunakan Hugging Face Inference API.
    Returns dict dengan label, confidence, dan semua skor.
    """
    
    # Validasi API key
    if not HUGGINGFACE_API_KEY:
        return {
            "emotion": "Netral",
            "confidence": 0.0,
            "all_scores": {label: 0.0 for label in labels},
            "error": "HUGGINGFACE_API_KEY not configured. Please set it in Railway environment variables."
        }
    
    # Header untuk autentikasi
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Payload request
    payload = {
        "inputs": text,
        "options": {
            "wait_for_model": True  # Tunggu jika model sedang loading (cold start)
        }
    }
    
    try:
        # Request ke Hugging Face API
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30  # Timeout 30 detik
        )
        
        # Sukses
        if response.status_code == 200:
            result = response.json()
            
            # Format response dari HF API
            # Format: [[{"label": "LABEL_0", "score": 0.95}, ...]]
            if isinstance(result, list) and len(result) > 0:
                predictions = result[0]  # Ambil prediksi pertama
                
                # Map LABEL_0, LABEL_1, ... ke label asli
                all_scores = {}
                max_score = 0.0
                predicted_emotion = labels[0]  # Default: "Senang"
                
                for pred in predictions:
                    # Extract index dari "LABEL_X"
                    label_idx = int(pred['label'].split('_')[1])
                    emotion_label = labels[label_idx]
                    score = pred['score']
                    
                    all_scores[emotion_label] = float(score)
                    
                    # Track prediksi tertinggi
                    if score > max_score:
                        max_score = score
                        predicted_emotion = emotion_label
                
                return {
                    "emotion": predicted_emotion,
                    "confidence": float(max_score),
                    "all_scores": all_scores
                }
        
        # Error dari API
        elif response.status_code == 503:
            # Model sedang loading
            return {
                "emotion": "Netral",
                "confidence": 0.0,
                "all_scores": {label: 0.0 for label in labels},
                "error": "Model is loading. Please try again in 20-30 seconds."
            }
        else:
            return {
                "emotion": "Netral",
                "confidence": 0.0,
                "all_scores": {label: 0.0 for label in labels},
                "error": f"API error {response.status_code}: {response.text}"
            }
        
    except requests.exceptions.Timeout:
        return {
            "emotion": "Netral",
            "confidence": 0.0,
            "all_scores": {label: 0.0 for label in labels},
            "error": "Request timeout. Model might be loading (cold start)."
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "emotion": "Netral",
            "confidence": 0.0,
            "all_scores": {label: 0.0 for label in labels},
            "error": f"Network error: {str(e)}"
        }
    
    except Exception as e:
        return {
            "emotion": "Netral",
            "confidence": 0.0,
            "all_scores": {label: 0.0 for label in labels},
            "error": f"Unexpected error: {str(e)}"
        }