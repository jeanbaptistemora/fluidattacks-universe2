let
  pkg_override = is_pkg: new_pkg: let
    override = x:
      if is_pkg x
      then new_pkg
      else pkg_override is_pkg new_pkg x;
  in
    pkg:
      if pkg ? overridePythonAttrs
      then
        pkg.overridePythonAttrs (
          builtins.mapAttrs (_: value:
            if builtins.isList value
            then map override value
            else override value)
        )
      else pkg;
in
  pkg_override
