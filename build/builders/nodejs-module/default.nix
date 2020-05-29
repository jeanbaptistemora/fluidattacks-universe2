pkgs:

{ moduleName
, requirement
}:

  pkgs.stdenv.mkDerivation rec {
    name = "nodejs-module-${moduleName}";
    inherit requirement;

    srcGenericShellOptions = ../../include/generic/shell-options.sh;
    srcGenericDirStructure = ../../include/generic/dir-structure.sh;

    builder = ./builder.sh;
    propagatedBuildInputs = with pkgs; [ nodejs ];
  }
