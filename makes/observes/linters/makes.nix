{ inputs
, ...
}:
{
  lintPython = {
    modules = {
      observesCodeEtl = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/code_etl";
      };
      observesCodeEtlTests = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/tests";
      };
    };
  };
}
