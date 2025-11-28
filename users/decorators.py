from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    """
    Decorator untuk memastikan hanya admin yang bisa mengakses view tertentu.
    User biasa akan di-redirect ke halaman not_admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Cek apakah user sudah login
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        # Cek apakah user adalah admin
        if request.user.role != 'admin':
            return redirect('dashboard:not_admin')
        
        # Jika admin, lanjutkan ke view
        return view_func(request, *args, **kwargs)
    
    return wrapper