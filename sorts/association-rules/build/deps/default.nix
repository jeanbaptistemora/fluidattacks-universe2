{
  lib,
  python_pkgs,
}: let
  mlxtend = python_pkgs.mlxtend.overridePythonAttrs (
    old: rec {
      version = "0.19.0";
      src = lib.fetchFromGitHub {
        owner = "rasbt";
        repo = old.pname;
        rev = "v0.19.0";
        sha256 = "XC1ZYRyDgrNfS3B6gCHTv/Znvu1uAJusCMZ9sj/9XGE=";
      };
      meta = old.meta // {broken = false;};
      doCheck = false;
    }
  );
in
  python_pkgs // {inherit mlxtend;}
