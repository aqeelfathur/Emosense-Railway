from django.db import models
from django.conf import settings
import random
import string
from django.utils import timezone

class CekEmosi(models.Model):
    """
    Model untuk menyimpan hasil deteksi emosi
    Hanya tersimpan jika user sudah login
    """
    id_cek = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='emotion_checks'
    )
    link_yt = models.CharField(max_length=200, null=True, blank=True)
    hasil_deteksi = models.CharField(max_length=20)
    detail_hasil = models.TextField()  # JSON string
    jumlah_comment = models.IntegerField(default=1)
    tanggal = models.DateTimeField(auto_now_add=True)
    
    # Field tambahan
    input_text = models.TextField(null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'cek_emosi'
        ordering = ['-tanggal']
        verbose_name = 'Deteksi Emosi'
        verbose_name_plural = 'Riwayat Deteksi Emosi'
    
    def __str__(self):
        return f"{self.id_cek} - {self.user.username} - {self.hasil_deteksi}"
    
    @staticmethod
    def generate_id():
        """Generate ID unik untuk cek emosi"""
        timestamp = timezone.now().strftime('%y%m%d%H%M')
        random_str = ''.join(random.choices(string.digits, k=4))
        return f"CE{timestamp[-6:]}{random_str}"[:10]