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
    import_and_run tap_bugsnag.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.bugsnag.env.runtime}"
    ];
  };
  name = "observes-singer-tap-bugsnag-bin";
}
