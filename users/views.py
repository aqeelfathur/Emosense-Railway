from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Cek role user
            if user.role == 'admin':
                messages.success(request, f'Selamat datang kembali, {user.username} (Admin)')
                return render(request, 'dashboard/home.html')
            else:
                messages.success(request, f'Selamat datang kembali, {user.username}')
                return render(request, 'emotion/cek_emosi.html')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validasi dasar
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Semua kolom harus diisi.')
            return render(request, 'users/register.html')

        if password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar.')
            return render(request, 'users/register.html') 

         # Simpan user baru (default role = user)
        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),  # pastikan password di-hash
                role='user',
            )
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('users:login')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')
            return render(request, 'users/register.html')  

    # GET request → tampilkan form register
    return render(request, 'users/register.html')

def register_api(request):
    if request.method == 'POST':
        data = request.POST
        id_user = data.get('id_user')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username sudah digunakan.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email sudah terdaftar.'}, status=400)

        user = User.objects.create(
            id_user=id_user,
            username=username,
            email=email,
            password=make_password(password),
            role='user',
        )
        return JsonResponse({'status': 'success', 'message': 'Registrasi berhasil!'})
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)
