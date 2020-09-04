pkgs:

rec {
  srcExternalANTLR4 = pkgs.fetchurl {
    url = "https://www.antlr.org/download/antlr-4.8-complete.jar";
    sha256 = "0nms976cnqyr1ndng3haxkmknpdq6xli4cpf4x4al0yr21l9v93k";
  };
}
