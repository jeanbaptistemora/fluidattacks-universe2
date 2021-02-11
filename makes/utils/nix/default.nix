_: pkgs:
let
  toLower = pkgs.lib.strings.toLower;
in
rec {
  # Return true if string is a nix store path
  isStorePath = string: "/nix/store" == pkgs.lib.strings.substring 0 10 string;

  # Write each item on the list to a line in the file, return the file
  listToFileWithTrailinNewLine = list: builtins.toFile "list" (
    builtins.concatStringsSep "\n" (list ++ [ "" ])
  );

  # Read a file handling edge cases
  readFile = expr:
    if isStorePath expr
    then builtins.readFile expr
    else if builtins.isString expr
    then expr
    else abort "Expected a store path or a string, got: ${builtins.typeOf expr}";

  # Sort a list based on ascii code point
  sort = builtins.sort (a: b: a < b);

  # Sort a list based on ascii code point ignoring case
  sortCaseless = builtins.sort (a: b: toLower a < toLower b);
}
