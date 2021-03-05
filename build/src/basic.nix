rec {

  # Build
  srcEnv = ../include/env.sh;
  srcIncludeCli = ../include/cli.sh;
  srcIncludeGenericShellOptions = ../include/generic/shell-options.sh;
  srcIncludeGenericDirStructure = ../include/generic/dir-structure.sh;

  # Common
  srcIncludeHelpersCommon = ../include/helpers/common.sh;
  srcIncludeHelpersCommonGitlab = ../include/helpers/common.gitlab.sh;
  srcIncludeCommonJobs = ../include/jobs/common.sh;

  # Airs
  srcIncludeHelpersAirs = ../include/helpers/airs.sh;
  srcIncludeHelpersAirsBlog = ../include/helpers/airs-blog.sh;
  srcIncludeHelpersAirsDeploy = ../include/helpers/airs-deploy.sh;
  srcIncludeAirsJobs = ../include/jobs/airs.sh;

  # Asserts
  srcIncludeHelpersAsserts = ../include/helpers/asserts.sh;
  srcIncludeAssertsJobs = ../include/jobs/asserts.sh;

  # Integrates
  srcIncludeHelpersIntegrates = ../include/helpers/integrates.sh;
  srcIncludeIntegratesJobs = ../include/jobs/integrates.sh;

  # Observes
  srcIncludeHelpersObserves = ../include/helpers/observes.sh;
  srcIncludeObservesJobs = ../include/jobs/observes.sh;

  # Services
  srcIncludeHelpersServices = ../include/helpers/services.sh;
}
