pkgs:
string:
  with pkgs.lib;
  strings.concatStrings
    (lists.filter
      (char:
        lists.any
          (x: x == char)
          (lists.concatLists
            (lists.map strings.stringToCharacters [
              "abcdefghijklmnopqrstuvwxyz"
              "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
              "0123456789"
              "."
            ])))
      (strings.stringToCharacters string))
