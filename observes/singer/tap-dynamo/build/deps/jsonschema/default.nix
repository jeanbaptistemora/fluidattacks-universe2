{
  lib,
  python_pkgs,
}:
python_pkgs.jsonschema.overridePythonAttrs (
  old: rec {
    version = "3.2.0";
    SETUPTOOLS_SCM_PRETEND_VERSION = version;
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "yKhbKNN3zHc35G4tnytPRO48Dh3qxr9G3e/HGH0weXo=";
    };
    # Some tests (of sub-deps) are not deterministic i.e. depends on env user
    # TODO: skip only non deterministic tests
    doCheck = false;
  }
)
