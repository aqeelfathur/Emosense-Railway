from django import forms

class TextEmotionForm(forms.Form):
    """Form untuk input teks manual"""
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tulis atau paste teks yang ingin dianalisis emosinya...',
            'required': True
        }),
        label='Masukkan Teks',
        max_length=5000
    )

class YouTubeEmotionForm(forms.Form):
    """Form untuk input link YouTube"""
    youtube_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.youtube.com/watch?v=...',
            'required': True
        }),
        label='Link Video YouTube'
    )
    max_comments = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 10,
            'max': 100,
            'value': 50
        }),
        label='Jumlah Komentar (max 100)',
        initial=50,
        min_value=10,
        max_value=100
    )