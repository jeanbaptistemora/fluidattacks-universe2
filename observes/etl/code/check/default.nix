{self_pkg}: let
  build_check = check:
    self_pkg.overridePythonAttrs (
      old: {
        checkPhase = [old."${check}"];
      }
    );
in {
  tests = build_check "test_check";
  types = build_check "type_check";
}
