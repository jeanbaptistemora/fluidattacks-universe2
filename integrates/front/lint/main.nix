{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-front-lint";
  searchPaths = {
    bin = [
      outputs."/integrates/front/lint/eslint"
      outputs."/integrates/front/lint/stylelint"
    ];
    source = [
      outputs."/common/utils/lint-npm-deps"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
