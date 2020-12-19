# Replace env vars in the input string

pkgs:

{
  content,
  envVars,
}:

let
  make = import ../../../makes/utils/make pkgs;
in
  make (envVars // {
    builder = ./builder.sh;
    buildInputs = [ pkgs.envsubst ];
    envFile = builtins.toFile "content" content;
  })
