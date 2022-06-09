let
  pkg_override = is_pkg: new_pkg: let
    override = x:
      if x ? overridePythonAttrs && is_pkg x
      then new_pkg
      else pkg_override is_pkg new_pkg x;
  in
    pkg:
      if pkg ? overridePythonAttrs
      then
        pkg.overridePythonAttrs (
          old: {
            checkInputs = map override (old.checkInputs or []);
            buildInputs = map override (old.buildInputs or []);
            nativeBuildInputs = map override (old.nativeBuildInputs or []);
            propagatedBuildInputs = map override (old.propagatedBuildInputs or []);
            pythonPath = map override (old.pythonPath or []);
          }
        )
      else pkg;
in
  pkg_override
