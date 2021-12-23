{ fromYaml
, inputs
, makeDerivation
, projectPath
, ...
}:
let
  lib = inputs.nixpkgs.lib;

  translationsFiles = builtins.attrNames (builtins.readDir
    (projectPath "/skims/static/translations/criteria/vulnerabilities"));

  translationsKeys = builtins.map
    (x:
      builtins.attrNames (fromYaml (builtins.readFile
        (projectPath "/skims/static/translations/criteria/vulnerabilities" + "/${x}"))))
    # Exclude Words.yaml file
    (lib.lists.take ((builtins.length translationsFiles) - 1) translationsFiles);

  trimKeys = builtins.map
    (x: lib.lists.unique (builtins.concatMap
      (
        y: lib.lists.drop (builtins.length (lib.strings.splitString "." y) - 1)
          (lib.strings.splitString "." y)
      )
      x))
    (translationsKeys);

  necesaryKeys = builtins.map
    (builtins.map (y:
      if (y == "description" || y == "impact" || y == "recommendation" || y == "threat")
      then true
      else y))
    (trimKeys);

  areKeysComplete = lib.lists.all (keys: keys == 4)
    (builtins.map (lib.lists.count (y: y == true)) (necesaryKeys));

  areTranslationsComplete = keysComplete:
    if (keysComplete)
    then true
    else abort "\n[ERROR] Translations: The fields of Translations are incomplete, please check that the fields required by the ASM are filled in all the translations";
in
makeDerivation {
  env = { envTranslationsComplete = areTranslationsComplete areKeysComplete; };
  builder = ''
    info "Translations are complete."
    touch $out
  '';
  name = "criteria-translations";
}
