def after_all(context):
    """Cleanup yang dijalankan sekali setelah semua test"""
    # Tutup browser
    context.browser.quit()