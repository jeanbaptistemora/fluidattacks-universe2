{ inputs
, makeScript
, ...
}:
let
  nosql = inputs.nixpkgs.appimageTools.wrapType2
    {
      name = "nosql";
      src = inputs.nixpkgs.fetchurl {
        name = "NosqlWorkbench";
        url = "https://s3.amazonaws.com/nosql-workbench/NoSQL%20Workbench-linux-x86_64-3.2.0.AppImage";
        sha512 = "18j6vpv7qazj5dcw4fn2178rjh90dq8c9h3d2msc3j39fnivbb0n1aa8wwkxwgc3yrnq9ciqhwk6lwny8542m8fkj3n3fmrggj3j705";
      };
    };
in
makeScript {
  replace = {
    __argNoSql__ = nosql;
  };
  name = "nosql_workbenck";
  searchPaths = { bin = [ inputs.nixpkgs.bash ]; };
  entrypoint = "bash __argNoSql__/bin/nosql";
}
