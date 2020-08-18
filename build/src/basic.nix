rec {
  srcEnv = ../include/env.sh;
  srcIncludeCli = ../include/cli.sh;
  srcIncludeGenericShellOptions = ../include/generic/shell-options.sh;
  srcIncludeGenericDirStructure = ../include/generic/dir-structure.sh;

  srcIncludeHelpersCommon = ../include/helpers/common.sh;
  srcIncludeHelpersIntegrates = ../include/helpers/integrates.sh;
  srcIncludeHelpersSkims = ../include/helpers/skims.sh;
  srcIncludeHelpersForces = ../include/helpers/forces.sh;

  srcIncludeCommonJobs = ../include/jobs/common.sh;
  srcIncludeIntegratesJobs = ../include/jobs/integrates.sh;
  srcIncludeIntegratesLintersJobs = ../include/jobs/integrates.linters.sh;
  srcIncludeSkimsJobs = ../include/jobs/skims.sh;
  srcIncludeForcesJobs = ../include/jobs/forces.sh;
  srcIncludeReviewsJobs = ../include/jobs/reviews.sh;
}
