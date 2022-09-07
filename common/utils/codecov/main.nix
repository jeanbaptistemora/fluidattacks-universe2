# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeDerivation,
  ...
}:
makeDerivation {
  env.envSrc = inputs.nixpkgs.fetchurl {
    url = "https://uploader.codecov.io/v0.2.1/linux/codecov";
    sha256 = "14kff14mk11kkf7jisr4c8r9bvdyx212drgb2v435blhafrxnpwb";
  };
  builder = ''
    mkdir -p $out/bin
    copy $envSrc $out/bin/codecov
    chmod +x $out/bin/codecov
  '';
  name = "codecov";
}
