pkgs:

rec {
  srcCiScriptsHelpersOthers = ../../ci-scripts/helpers/others.sh;
  srcCiScriptsHelpersSops = ../../ci-scripts/helpers/sops.sh;
  srcEnv = ../include/env.sh;
  srcIncludeCli = ../include/cli.sh;
  srcIncludeGenericShellOptions = ../include/generic/shell-options.sh;
  srcIncludeGenericDirStructure = ../include/generic/dir-structure.sh;
  srcIncludeHelpers = ../include/helpers.sh;
  srcIncludeJobs = ../include/jobs.sh;
}
