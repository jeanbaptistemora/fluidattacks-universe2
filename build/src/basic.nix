rec {
  # Build
  srcEnv = ../include/env.sh;
  srcIncludeCli = ../include/cli.sh;
  srcIncludeGenericShellOptions = ../include/generic/shell-options.sh;
  srcIncludeGenericDirStructure = ../include/generic/dir-structure.sh;

  # Common
  srcIncludeHelpersCommon = ../include/helpers/common.sh;
  srcIncludeCommonJobs = ../include/jobs/common.sh;

  # Forces
  srcIncludeHelpersForces = ../include/helpers/forces.sh;
  srcIncludeForcesJobs = ../include/jobs/forces.sh;

  # Integrates
  srcIncludeHelpersIntegrates = ../include/helpers/integrates.sh;
  srcIncludeIntegratesJobs = ../include/jobs/integrates.sh;
  srcIncludeIntegratesLintersJobs = ../include/jobs/integrates.linters.sh;

  # Reviews
  srcIncludeReviewsJobs = ../include/jobs/reviews.sh;

  # Serves
  srcIncludeHelpersServes = ../include/helpers/serves.sh;
  srcIncludeHelpersAnalytics = ../include/helpers/analytics.sh;
  srcIncludeServesJobs = ../include/jobs/serves.sh;

  # Skims
  srcIncludeHelpersSkims = ../include/helpers/skims.sh;
  srcIncludeSkimsJobs = ../include/jobs/skims.sh;
}
