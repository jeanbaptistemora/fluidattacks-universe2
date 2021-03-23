{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envBuilt = [
      packages.integrates.front.lint.eslint
      packages.integrates.front.lint.stylelint
    ];
  };
  builder = path "/makes/packages/integrates/front/lint/builder.sh";
  name = "integrates-front-lint";
}
