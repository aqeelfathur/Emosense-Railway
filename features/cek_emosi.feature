Feature: Cek Emosi dari Komentar YouTube
  As a user
  I want to check the emotion from YouTube comments
  So that I can know the emotional tendency from the video comments

  Scenario: Analisis emosi dari komentar YouTube
    Given I am on "cek_emosi"
    Then I should see "Analisis emosi dari komentar YouTube menggunakan AI"

    When I fill in "youtube_url" with "https://www.youtube.com/watch?v=Sq1s564ukTI"
    Then the "youtube_url" field should contain "https://www.youtube.com/watch?v=Sq1s564ukTI"

    When I fill in "max_comments" with "50"
    Then the "max_comments" field should contain "50"

    When I press "Analisis Komentar"
    Then I should see "Hasil Analisis"
    And I should see "Daftar Komentar & Emosi"
