Feature: Lihat Dashboard Admin
  As an Admin
  I want to view dashboard content
  So that I can monitor system performance and statistics

  Scenario: Admin melihat statistik di dashboard
    Given browser terbuka
    And I go to "http://127.0.0.1:8000/dashboard"
    And admin sudah login

    Then I should see "Selamat Datang"
    And I should see "Total Akun Terdaftar"
    And I should see "Total Deteksi Emosi"
    And I should see "User Terbaru"
    And I should see "Deteksi Emosi Terbaru"
