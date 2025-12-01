Feature: Kelola History Deteksi Emosi
  As a Admin
  I want to view the emotion analysis history of users
  So that I can monitor user activity and system usage

  Background:
    Given I am logged in as admin
    And I am on "/dashboard"
    Then I should see "Dashboard Admin Emosense"

  Scenario: Admin melihat halaman kelola history
    When I go to "/dashboard/kelola_history"
    Then I should see "Kelola History Deteksi Emosi"

  Scenario: Admin melihat detail history deteksi emosi
    Given I go to "/dashboard/kelola_history"
    And I should see "Kelola History Deteksi Emosi"
    When I select "lihat" from row "CE26061454"
    Then I should see "Detail History Deteksi"
    When I select "Kembali"
    Then I should see "Kelola History Deteksi Emosi"

  Scenario: Admin menghapus history deteksi emosi
    Given I go to "/dashboard/kelola_history"
    And I should see "Kelola History Deteksi Emosi"
    When I select "Hapus" from row "CE26061454"
    Then I should see "Yakin hapus history"
    When I press "Iya"
    Then I should see "History CE26061454 dari user admin1 berhasil dihapus!"

  Scenario: Admin membatalkan penghapusan history
    Given I go to "/dashboard/kelola_history"
    And I should see "Kelola History Deteksi Emosi"
    When I select "Hapus" from row "CE25134751"
    Then I should see "Yakin hapus history"
    When I press "Tidak"
    Then I should see "Kelola History Deteksi Emosi"