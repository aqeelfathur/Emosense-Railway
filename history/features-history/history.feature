Feature: Lihat History
  As a User
  I want to view my previous emotion analysis history
  So that I can review my past results

  Background:
    Given there is a test user "bdd_user" with password "bdd_password"
    And there is a sample analysis with id "ANALISIS_1" for user "bdd_user"

  Scenario: Melihat riwayat dan membuka detail analisis
    Given I am on "halaman_history"
    Then I should see "Riwayat Deteksi"
    And I should see "Lihat semua hasil analisis emosi Anda"

    When I select "analisis_tertentu" from "list_history"
    Then I should see the detail modal
    And I should see "Detail Analisis"
    And I should see "Detail Skor Semua Emosi"

    When I reload the page
    Then I should see "Riwayat Deteksi"
