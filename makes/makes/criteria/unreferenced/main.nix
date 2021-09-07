{ fromYaml
, inputs
, makeDerivation
, makeScript
, projectPath
, ...
}:
let
  lib = inputs.nixpkgs.lib;

  # Load data
  requirements = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/requirements/data.yaml"
    )
  );
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"
    )
  );

  # List of referenced items
  references = { field, data }: lib.lists.unique (
    lib.lists.flatten (
      builtins.map (x: x.${field}) (builtins.attrValues data)
    )
  );

  # True if item id exists in data, false otherwise
  isReferenced = { id, data }:
    builtins.any (item: item == id) data;

  # List of unreferenced items
  unreferenced = { field, referencedData, data }:
    builtins.attrNames (
      lib.filterAttrs
        (id: _: ! isReferenced {
          inherit id;
          data = references {
            inherit field;
            data = referencedData;
          };
        })
        data
    );

  # JSON output
  output = makeDerivation {
    env = {
      envUnreferenced = builtins.toJSON {
        requirements = unreferenced {
          field = "requirements";
          referencedData = vulnerabilities;
          data = requirements;
        };
      };
    };
    searchPaths.bin = [ inputs.nixpkgs.jq ];
    builder = ''
      echo "$envUnreferenced" | jq . > "$out"
    '';
    name = "criteria-unreferenced";
  };
in
makeScript {
  replace = {
    __argOutput__ = output;
  };
  entrypoint = ''
    cat __argOutput__
  '';
  name = "criteria-unreferenced";
}
