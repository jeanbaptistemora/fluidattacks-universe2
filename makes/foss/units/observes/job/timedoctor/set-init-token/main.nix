{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.product.observes.bin.service.timedoctor-tokens ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-timedoctor-set-init-token";
  entrypoint = ./entrypoint.sh;
}
