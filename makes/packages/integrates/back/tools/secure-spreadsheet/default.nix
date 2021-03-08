{ buildNodeRequirements
, nixpkgs
, ...
}:
buildNodeRequirements {
  name = "integrates-back-tools-secure-spreadsheet";
  node = nixpkgs.nodejs;
  requirements = {
    direct = [
      "secure-spreadsheet@0.1.0"
    ];
    inherited = [
      "adler-32@1.2.0"
      "cfb@1.2.0"
      "commander@2.20.3"
      "core-util-is@1.0.2"
      "crc-32@1.2.0"
      "csv-parse@2.5.0"
      "exit-on-epipe@1.0.1"
      "get-stdin@6.0.0"
      "immediate@3.0.6"
      "inherits@2.0.4"
      "isarray@1.0.0"
      "jszip@3.5.0"
      "lie@3.3.0"
      "lodash@4.17.20"
      "pako@1.0.11"
      "printj@1.1.2"
      "process-nextick-args@2.0.1"
      "readable-stream@2.3.7"
      "safe-buffer@5.1.2"
      "sax@1.2.4"
      "set-immediate-shim@1.0.1"
      "string_decoder@1.1.1"
      "util-deprecate@1.0.2"
      "xlsx-populate@1.21.0"
    ];
  };
}
