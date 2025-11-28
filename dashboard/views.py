from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from users.models import User
from emotion.models import CekEmosi
from users.decorators import admin_required

@admin_required
def dashboard_home(request):

    #Total user dan total cek emosi (Statistik Cards)
    total_users = User.objects.count()
    total_cek_emosi = CekEmosi.objects.count()

    #5 User Terbaru (Recent 5 Users)
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    #5 Cek Emosi Terbaru (Recent 5 Cek Emosi)
    recent_cek_emosi = CekEmosi.objects.select_related('user').order_by('-tanggal')[:5]
    
    context = {
        'total_users': total_users,
        'total_cek_emosi': total_cek_emosi,
        'recent_users': recent_users,
        'recent_cek_emosi': recent_cek_emosi,
    }

    return render(request, 'dashboard/home.html', context)

@admin_required
def dashboard_kelola_history(request):
    # Get all cek emosi with pagination support
    all_history = CekEmosi.objects.select_related('user').order_by('-tanggal')
    
    context = {
        'history_list': all_history,
    }
    
    return render(request, 'dashboard/kelola_history.html', context)


@admin_required
def dashboard_kelola_user(request):
    # Get all users
    all_users = User.objects.annotate(
        total_deteksi=Count('emotion_checks')
    ).order_by('-date_joined')
    
    context = {
        'users_list': all_users,
    }
    
    return render(request, 'dashboard/kelola_user.html', context)

@admin_required
def dashboard_edit_user(request, id_user):
    """View untuk edit user"""
    user = get_object_or_404(User, id_user=id_user)
    
    if request.method == 'POST':
        # Ambil data dari form
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        
        # Validasi username (cek duplikat kecuali user sendiri)
        if User.objects.filter(username=username).exclude(id_user=id_user).exists():
            messages.error(request, 'Username sudah digunakan!')
            return redirect('dashboard:edit_user', id_user=id_user)
        
        # Validasi email (cek duplikat kecuali user sendiri)
        if User.objects.filter(email=email).exclude(id_user=id_user).exists():
            messages.error(request, 'Email sudah digunakan!')
            return redirect('dashboard:edit_user', id_user=id_user)
        
        # Update data user
        user.username = username
        user.email = email
        user.role = role
        
        # Update password jika diisi
        if password:
            user.set_password(password)
        
        user.save()
        
        messages.success(request, f'User {username} berhasil diupdate!')
        return redirect('dashboard:kelola_user')
    
    context = {
        'user_data': user,
    }
    
    return render(request, 'dashboard/edit_user.html', context)

@admin_required
def dashboard_delete_user(request, id_user):
    """View untuk delete user"""
    user = get_object_or_404(User, id_user=id_user)
    
    # Cegah admin menghapus dirinya sendiri
    if user.id_user == request.user.id_user:
        messages.error(request, 'Anda tidak bisa menghapus akun sendiri!')
        return redirect('dashboard:kelola_user')
    
    username = user.username
    user.delete()
    
    messages.success(request, f'User {username} berhasil dihapus!')
    return redirect('dashboard:kelola_user')

@admin_required
def dashboard_detail_history(request, id_cek):
    """View untuk melihat detail history deteksi"""
    history = get_object_or_404(CekEmosi.objects.select_related('user'), id_cek=id_cek)
    
    # Parse detail_hasil dari JSON string
    import json
    try:
        detail_hasil = json.loads(history.detail_hasil)
    except:
        detail_hasil = {}
    
    context = {
        'history': history,
        'detail_hasil': detail_hasil,
    }
    
    return render(request, 'dashboard/detail_history.html', context)

@admin_required
def dashboard_delete_history(request, id_cek):
    """View untuk delete history deteksi"""
    history = get_object_or_404(CekEmosi, id_cek=id_cek)
    
    user_name = history.user.username
    id_history = history.id_cek
    history.delete()
    
    messages.success(request, f'History {id_history} dari user {user_name} berhasil dihapus!')
    return redirect('dashboard:kelola_history')

def not_admin_view(request):
    return render(request, 'dashboard/not_admin.html')