# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_mailchimp.cli main "$@"
  '';
  searchPaths = {
    bin = [inputs.nixpkgs.python38];
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.mailchimp.env.runtime}"
    ];
  };
  name = "observes-singer-tap-mailchimp-bin";
}
