{self_pkg}: let
  build_check = check:
    self_pkg.overridePythonAttrs (
      old: {
        checkPhase = [old."${check}"];
      }
    );
  runtime_check = self_pkg.overridePythonAttrs (
    _: {
      doCheck = false;
    }
  );
in {
  arch = build_check "arch_check";
  runtime = runtime_check;
  tests = build_check "test_check";
  types = build_check "type_check";
}
