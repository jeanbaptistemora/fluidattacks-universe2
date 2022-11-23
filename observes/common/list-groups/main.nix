{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  searchPaths = {
    source = [
      (outputs."${inputs.observesIndex.common.asm_dal.bin}")
    ];
  };
  name = "observes-list-groups";
  template = ./template.sh;
}
