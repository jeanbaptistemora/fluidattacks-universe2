{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs-lint";
  searchPaths = {
    source = [
      outputs."/common/utils/lint-npm-deps"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
