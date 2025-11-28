from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from emotion.models import CekEmosi
from emotion.forms import TextEmotionForm, YouTubeEmotionForm
from datetime import datetime, timedelta
import json
import csv


@login_required
def history_list(request):
    """
    Tampilkan riwayat deteksi emosi
    - User biasa: hanya lihat riwayat sendiri
    - Admin: lihat semua riwayat
    """
    # Filter berdasarkan role
    if request.user.role == 'admin':
        emotions = CekEmosi.objects.all()
    else:
        emotions = CekEmosi.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        emotions = emotions.filter(
            Q(id_cek__icontains=search_query) |
            Q(hasil_deteksi__icontains=search_query) |
            Q(link_yt__icontains=search_query) |
            Q(input_text__icontains=search_query)
        )

    # Filter by emotion
    emotion_filter = request.GET.get('emotion', '')
    if emotion_filter:
        emotions = emotions.filter(hasil_deteksi=emotion_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        emotions = emotions.filter(tanggal__gte=date_from)
    if date_to:
        emotions = emotions.filter(tanggal__lte=date_to)

    # Pagination
    paginator = Paginator(emotions, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    stats = {
        'total': emotions.count(),
        'senang': emotions.filter(hasil_deteksi='Senang').count(),
        'sedih': emotions.filter(hasil_deteksi='Sedih').count(),
        'marah': emotions.filter(hasil_deteksi='Marah').count(),
        'takut': emotions.filter(hasil_deteksi='Takut').count(),
        'netral': emotions.filter(hasil_deteksi='Netral').count(),
        
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'search_query': search_query,
        'emotion_filter': emotion_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'history/history.html', context)


@login_required
@login_required
def history_detail(request, id_cek):
    """Detail hasil deteksi emosi - return JSON"""
    emotion = get_object_or_404(CekEmosi, id_cek=id_cek)
    
    # Check permission
    if request.user.role != 'admin' and emotion.user != request.user:
        return JsonResponse({
            'error': 'Tidak memiliki akses'
        }, status=403)
    
    data = {
        'id_cek': emotion.id_cek,
        'hasil_deteksi': emotion.hasil_deteksi,
        'detail_hasil': emotion.detail_hasil,  # sudah JSON string
        'confidence_score': emotion.confidence_score,
        'tanggal': emotion.tanggal.isoformat(),
        'link_yt': emotion.link_yt,
        'jumlah_comment': emotion.jumlah_comment,
        'input_text': emotion.input_text,
    }
    
    return JsonResponse(data)


@login_required
def history_delete(request, id_cek):
    """
    Hapus riwayat deteksi emosi
    """
    emotion = get_object_or_404(CekEmosi, id_cek=id_cek)
    
    # Check permission
    if request.user.role != 'admin' and emotion.user != request.user:
        return JsonResponse({
            'success': False, 
            'message': 'Tidak memiliki akses'
        }, status=403)
    
    if request.method == 'POST':
        emotion.delete()
        return JsonResponse({
            'success': True, 
            'message': 'Data berhasil dihapus'
        })
    
    return JsonResponse({
        'success': False, 
        'message': 'Method tidak valid'
    }, status=400)


@login_required
def history_export(request):
    """
    Export riwayat ke CSV
    """
    # Filter berdasarkan role
    if request.user.role == 'admin':
        emotions = CekEmosi.objects.all()
    else:
        emotions = CekEmosi.objects.filter(user=request.user)
    
    # Create CSV
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="history_emosi_{timestamp}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Username', 'Tanggal', 'Emosi', 
        'Confidence', 'Link YouTube', 'Jumlah Komentar'
    ])
    
    for emotion in emotions:
        writer.writerow([
            emotion.id_cek,
            emotion.user.username,
            emotion.tanggal.strftime('%Y-%m-%d %H:%M:%S'),
            emotion.hasil_deteksi,
            f"{emotion.confidence_score:.2f}%",
            emotion.link_yt or '-',
            emotion.jumlah_comment,
        ])
    
    return response
@login_required
def history_stats_api(request):
    """
    API untuk mendapatkan statistik emosi (untuk chart)
    """
    # Filter berdasarkan role
    if request.user.role == 'admin':
        emotions = CekEmosi.objects.all()
    else:
        emotions = CekEmosi.objects.filter(user=request.user)
    
    # Get date range (default: 7 hari terakhir)
    days = int(request.GET.get('days', 7))
    start_date = datetime.now() - timedelta(days=days)
    emotions = emotions.filter(tanggal__gte=start_date)
    
    # Aggregate by emotion
    emotion_counts = emotions.values('hasil_deteksi').annotate(
        count=Count('id_cek')
    )
    
    # Aggregate by date
    from django.db.models.functions import TruncDate
    date_counts = emotions.annotate(
        date=TruncDate('tanggal')
    ).values('date').annotate(
        count=Count('id_cek')
    ).order_by('date')
    
    data = {
        'emotion_distribution': list(emotion_counts),
        'timeline': [
            {
                'date': item['date'].strftime('%Y-%m-%d'),
                'count': item['count']
            } for item in date_counts
        ],
        'total': emotions.count(),
    }
    
    return JsonResponse(data)   
    