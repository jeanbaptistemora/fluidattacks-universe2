let
  src = import ./fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "77cbf0db0ac5dc065969d44aef2cf81776d11228";
    digest = "0lnqqbvb3dv2gmi2dgmqlxlfhb9hvj19llw5jcfd7nc02yqlk1k7";
  };
in
  import src { }
