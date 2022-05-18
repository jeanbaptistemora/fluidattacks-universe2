{self_pkg}: let
  build_check = check:
    self_pkg.overridePythonAttrs (
      old: {
        installCheckPhase = [old."${check}"];
      }
    );
in {
  types = build_check "type_check";
}
