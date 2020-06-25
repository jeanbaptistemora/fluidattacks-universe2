pkgs:

rec {
  srcExternalC3 = pkgs.fetchurl {
    url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
    sha256 = "163q1h40ck5ach1pyamcg3pk9lnf2dsmw8c6rqa9bzfsv2naq4in";
  };
}
