_: pkgs:
let
  toLower = pkgs.lib.strings.toLower;
in
rec {
  # Ensure the expression contents are read, paths are loaded, strings are left intact
  asContent = expr:
    if builtins.isPath expr
    then builtins.readFile expr
    else if builtins.isString expr
    then expr
    else abort "Expected a store path or a string, got: ${builtins.typeOf expr}";

  # Return true if string is a nix store path
  isStorePath = string: "/nix/store" == pkgs.lib.strings.substring 0 10 string;

  # Write each item on the list to a line in the file, return the file
  listToFileWithTrailinNewLine = list: builtins.toFile "list" (
    builtins.concatStringsSep "\n" (list ++ [ "" ])
  );

  # Sort a list based on ascii code point
  sort = builtins.sort (a: b: a < b);

  # Sort a list based on ascii code point ignoring case
  sortCaseless = builtins.sort (a: b: toLower a < toLower b);
}
