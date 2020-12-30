pkgs:

{
  name,
  path,
  product,
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgs;
in
  makeEntrypoint {
    arguments = {
      envPath = path;
      envProduct = product;
      envShell = "${pkgs.bash}/bin/bash";
      envTerraform = "${pkgs.terraform_0_13}/bin/terraform";
      envTflint = "${pkgs.tflint}/bin/tflint";
      envTflintConfig = ../../../../.tflint.hcl;
      envUtilsBashLibAws = import ../../../../makes/utils/bash-lib/aws pkgs;
    };
    location = "/bin/${name}";
    name = name;
    template = ../../../../makes/utils/bash-lib/terraform-test/entrypoint.sh;
  }
