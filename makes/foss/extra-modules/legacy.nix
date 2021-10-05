{ inputs
, projectPath
, ...
}:
{
  config = {
    inputs = {
      legacy = {
        path = rel:
          /. + (builtins.unsafeDiscardStringContext (projectPath "/")) + rel;
        importUtility = utility:
          import (projectPath "/makes/utils/${utility}")
            inputs.legacy.path
            inputs.nixpkgs;
      };
    };
  };
}
