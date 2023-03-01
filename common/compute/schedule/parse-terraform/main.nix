{
  inputs,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/compute/schedule/parse-terraform/src/__init__.py";
    __argSchedules__ = projectPath "/common/compute/schedule/data.yaml";
    __argSizes__ = projectPath "/common/compute/arch/sizes/data.yaml";
  };
  searchPaths.bin = [
    inputs.nixpkgs.python39
    inputs.nixpkgs.yq
  ];
  template = ./template.sh;
  name = "common-compute-schedule-parse-terraform";
}
