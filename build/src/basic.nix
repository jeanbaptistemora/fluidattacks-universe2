rec {

  # Build
  srcEnv = ../include/env.sh;
  srcIncludeCli = ../include/cli.sh;
  srcIncludeGenericShellOptions = ../include/generic/shell-options.sh;
  srcIncludeGenericDirStructure = ../include/generic/dir-structure.sh;

  # Common
  srcIncludeHelpersCommon = ../include/helpers/common.sh;

  # Airs
  srcIncludeHelpersAirs = ../include/helpers/airs.sh;
  srcIncludeHelpersAirsDeploy = ../include/helpers/airs-deploy.sh;
  srcIncludeAirsJobs = ../include/jobs/airs.sh;

  # Integrates
  srcIncludeIntegratesJobs = ../include/jobs/integrates.sh;
}
