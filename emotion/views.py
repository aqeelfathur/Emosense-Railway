from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from .models import CekEmosi
from emotion.forms import TextEmotionForm, YouTubeEmotionForm
from emotion.services.load_model import predict_emotion
from datetime import datetime, timedelta
import json
import csv

# ==========================================
# CEK EMOSI VIEWS (Bisa Guest)
# ==========================================

def cek_emosi(request):
    """
    Halaman utama cek emosi
    Bisa diakses tanpa login (guest)
    """
    text_form = TextEmotionForm()
    youtube_form = YouTubeEmotionForm()
    
    context = {
        'text_form': text_form,
        'youtube_form': youtube_form,
        'user_logged_in': request.user.is_authenticated
    }
    
    return render(request, 'emotion/cek_emosi.html', context)

def analyze_youtube(request):
    """
    API endpoint untuk analisis komentar YouTube
    Menggunakan Google API untuk fetch comments
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method tidak valid'}, status=400)
    
    youtube_url = request.POST.get('youtube_url', '').strip()
    max_comments = int(request.POST.get('max_comments', 50))
    
    if not youtube_url:
        return JsonResponse({'error': 'Link YouTube tidak boleh kosong'}, status=400)
    
    try:
        # Extract video ID dari URL
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return JsonResponse({'error': 'Format link YouTube tidak valid'}, status=400)
        
        # Fetch comments dari YouTube
        comments = fetch_youtube_comments(video_id, max_comments)
        
        if not comments:
            return JsonResponse({'error': 'Tidak ada komentar ditemukan'}, status=404)
        
        # Analisis emosi untuk setiap komentar
        emotion_counts = {
            'Senang': 0,
            'Marah': 0,
            'Sedih': 0,
            'Takut': 0,
            'Netral': 0
        }
        
        all_confidences = []
        comments_with_emotion = []
        
        for comment in comments:
            result = predict_emotion(comment)
            emotion_counts[result['emotion']] += 1
            all_confidences.append(result['confidence'])
            
            # Simpan detail setiap komentar
            comments_with_emotion.append({
                'text': comment,
                'emotion': result['emotion'],
                'confidence': result['confidence'] * 100,
                'all_scores': result['all_scores']
            })
        
        # Tentukan emosi dominan
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        avg_confidence = sum(all_confidences) / len(all_confidences) * 100
        
        # Hitung persentase masing-masing emosi
        total = len(comments)
        emotion_percentages = {
            emotion: (count / total * 100) for emotion, count in emotion_counts.items()
        }
        
        # Jika user login, simpan ke database
        saved_id = None
        if request.user.is_authenticated:
            emotion_data = CekEmosi(
                id_cek=CekEmosi.generate_id(),
                user=request.user,
                link_yt=youtube_url,
                hasil_deteksi=dominant_emotion,
                detail_hasil=json.dumps(emotion_percentages),
                jumlah_comment=total,
                confidence_score=avg_confidence
            )
            emotion_data.save()
            saved_id = emotion_data.id_cek
        
        response_data = {
            'success': True,
            'emotion': dominant_emotion,
            'confidence': avg_confidence,
            'all_scores': emotion_percentages,
            'total_comments': total,
            'emotion_counts': emotion_counts,
            'comments': comments_with_emotion,
            'saved': request.user.is_authenticated,
            'saved_id': saved_id,
            'message': 'Hasil tersimpan di riwayat' if request.user.is_authenticated else 'Login untuk menyimpan hasil'
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Terjadi kesalahan: {str(e)}'
        }, status=500)

def extract_video_id(url):
    """
    Extract video ID dari URL YouTube
    Support format:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    import re
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([^&\n]+)',
        r'(?:youtu\.be\/)([^&\n]+)',
        r'(?:youtube\.com\/embed\/)([^&\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def fetch_youtube_comments(video_id, max_results=50):
    """
    Fetch komentar dari YouTube menggunakan Google API
    """
    from googleapiclient.discovery import build
    from django.conf import settings
    
    try:
        youtube = build(
            settings.YOUTUBE_API_SERVICE_NAME,
            settings.YOUTUBE_API_VERSION,
            developerKey=settings.GOOGLE_API_KEY
        )
        
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(max_results, 100),
            order='relevance',
            textFormat='plainText'
        )
        
        response = request.execute()
        
        comments = []
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        return comments
        
    except Exception as e:
        print(f"Error fetching comments: {str(e)}")
        return []
