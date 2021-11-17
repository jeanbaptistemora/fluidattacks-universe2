{ makeContainerImage
, makeDerivation
, outputs
, inputs
, ...
}:
makeContainerImage {
  config = {
    Env = [
      "USER=jane"
    ];
    User = "jane:jane";
    WorkingDir = "/";
  };
  layers = [
    (makeDerivation {
      env = {
        envEtcGroup = ''
          jane:x:0:
          nobody:x:65534:
        '';
        envEtcGshadow = ''
          jane:*::
          nobody:*::
        '';
        envEtcPamdOther = ''
          account sufficient pam_unix.so
          auth sufficient pam_rootok.so
          password requisite pam_unix.so nullok sha512
          session required pam_unix.so
        '';
        envEtcPasswd = ''
          jane:x:0:0::/home/jane:${inputs.nixpkgs.bash}/bin/bash
          nobody:x:65534:65534:nobody:/homeless:/bin/false
        '';
        envEtcShadow = ''
          jane:!x:::::::
          nobody:!x:::::::
        '';
      };
      builder = ./setup_shadow.sh;
      name = "jane-container-images-customization";
    })
    outputs."/skims/process-group"
    (makeDerivation {
      builder = ./builder.sh;
      name = "skims-process-group-container";
    })
  ];
}
