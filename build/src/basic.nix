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
  srcIncludeHelpersAirsGeneric = ../include/helpers/airs-generic.sh;
  srcIncludeHelpersAirsImage = ../include/helpers/airs-image.sh;
  srcIncludeAirsJobs = ../include/jobs/airs.sh;

  # Asserts
  srcIncludeHelpersAsserts = ../include/helpers/asserts.sh;
  srcIncludeAssertsJobs = ../include/jobs/asserts.sh;

  # Forces
  srcIncludeHelpersForces = ../include/helpers/forces.sh;
  srcIncludeForcesJobs = ../include/jobs/forces.sh;

  # Melts
  srcIncludeHelpersMelts = ../include/helpers/melts.sh;
  srcIncludeJobsMelts = ../include/jobs/melts.sh;

  # Integrates
  srcIncludeHelpersIntegrates = ../include/helpers/integrates.sh;
  srcIncludeIntegratesJobs = ../include/jobs/integrates.sh;
  srcIncludeIntegratesLintersJobs = ../include/jobs/integrates.linters.sh;

  # Observes
  srcIncludeHelpersObserves = ../include/helpers/observes.sh;
  srcIncludeObservesJobs = ../include/jobs/observes.sh;

  # Reviews
  srcIncludeReviewsJobs = ../include/jobs/reviews.sh;

  # Serves
  srcIncludeHelpersServes = ../include/helpers/serves.sh;
  srcIncludeServesJobs = ../include/jobs/serves.sh;

  # Services
  srcIncludeHelpersServices = ../include/helpers/services.sh;

  # Skims
  srcIncludeHelpersSkimsProcess = ../include/helpers/skims.process.sh;
  srcIncludeHelpersSkims = ../include/helpers/skims.sh;
  srcIncludeSkimsJobs = ../include/jobs/skims.sh;

  # Sorts
  srcIncludeHelpersSorts = ../include/helpers/sorts.sh;
  srcIncludeSortsJobs = ../include/jobs/sorts.sh;
}
