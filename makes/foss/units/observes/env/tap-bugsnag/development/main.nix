{ makeTemplate
, inputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-bugsnag-development";
  searchPaths = {
    source = [
      inputs.product.observes-env-tap-bugsnag-runtime
    ];
  };
}
