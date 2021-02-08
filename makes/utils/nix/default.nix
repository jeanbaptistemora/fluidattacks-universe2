_: pkgs:
let
  toLower = pkgs.lib.strings.toLower;
in
{
  listToFileWithTrailinNewLine = list: builtins.toFile "list" (
    builtins.concatStringsSep "\n" (list ++ [ "" ])
  );
  sort = builtins.sort (a: b: a < b);
  sortCaseless = builtins.sort (a: b: toLower a < toLower b);
}
