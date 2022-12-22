let
  # recursive_override: (Derivation -> Bool) ->
  #                     (Derivation -> Derivation) ->
  #                     (Derivation -> Derivation)
  recursive_override = is_pkg: new_pkg: let
    # override: Derivation -> Derivation
    override = pkg:
      if is_pkg pkg
      then new_pkg pkg
      else recursive_override is_pkg new_pkg pkg;
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
  # no_check_python_pkg: Derivation -> Derivation
  no_check_python_pkg = pkg:
    pkg.overridePythonAttrs (
      _: {
        doCheck = false;
      }
    );
in {
  inherit recursive_override no_check_python_pkg;
  # replace_pkg: List[str] -> Derivation -> Derivation
  replace_pkg = names: new_pkg: recursive_override (x: (x ? overridePythonAttrs && builtins.elem x.pname names)) (_: new_pkg);
  no_check_override = _: recursive_override (x: (x ? overridePythonAttrs)) no_check_python_pkg;
  # override_python_pkgs: (PythonPkgs -> PythonPkgs) -> PythonPkgs -> PythonPkgs
  apply_python_pkgs_override = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  compose = functions: val: builtins.foldl' (x: f: f x) val functions;
}
