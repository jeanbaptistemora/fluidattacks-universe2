# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeDerivation,
  ...
}: let
  src = builtins.fetchTarball {
    url = "https://artifacts.opensearch.org/releases/core/opensearch/${version}/opensearch-min-${version}-linux-x64.tar.gz";
    sha256 = "1m01sdh1i9ldi719cnlsbi10mmypvmqjcj9xsyn7qpiq95nmwmzi";
  };
  version = "1.3.0";
in
  makeDerivation {
    builder = ./builder.sh;
    env = {
      envSrc = src;
    };
    name = "opensearch-pkg";
    searchPaths.bin = [inputs.nixpkgs.jdk11_headless];
  }
