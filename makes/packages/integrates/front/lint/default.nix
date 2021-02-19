{ integratesPkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  builder = path "/makes/packages/integrates/front/lint/builder.sh";
  envBuilt = [
    packages.integrates.front.lint.eslint
    packages.integrates.front.lint.stylelint
    packages.integrates.front.lint.tslint
  ];
  name = "integrates-front-lint";
}
