{ servesPkgs
, servesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path servesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path servesPkgs;
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "serves";
      target = "serves/users/airs/terraform";
    }}/bin/${name}";
  };
  name = "serves-users-airs-test";
  template = path "/makes/applications/serves/users/airs/test/entrypoint.sh";
}
