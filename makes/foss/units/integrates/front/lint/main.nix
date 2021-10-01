{ makeDerivationParallel
, outputs
, ...
}:
makeDerivationParallel {
  dependencies = [
    outputs."/integrates/front/lint/eslint"
    outputs."/integrates/front/lint/stylelint"
  ];
  name = "integrates-front-lint";
}
