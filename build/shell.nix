let
  pkgs = import ./pkgs/stable.nix;

  modules.build.dependencies =  import ./dependencies pkgs;
in
  with modules.build;

  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = dependencies.all;

    pyPkgAnalyticsStreamerInfrastructure = dependencies.python.analytics.singer.streamerInfrastructure;
    pyPkgAnalyticsStreamerIntercom = dependencies.python.analytics.singer.streamerIntercom;
    pyPkgAnalyticsStreamerMandrill = dependencies.python.analytics.singer.streamerMandrill;
    pyPkgAnalyticsStreamerPcap = dependencies.python.analytics.singer.streamerPcap;
    pyPkgAnalyticsStreamerRingcentral = dependencies.python.analytics.singer.streamerRingcentral;
    pyPkgAnalyticsTapAwsdynamodb = dependencies.python.analytics.singer.tapAwsdynamodb;
    pyPkgAnalyticsTapCsv = dependencies.python.analytics.singer.tapCsv;
    pyPkgAnalyticsTapCurrrencyconverterapi = dependencies.python.analytics.singer.tapCurrrencyconverterapi;
    pyPkgAnalyticsTapFormstack = dependencies.python.analytics.singer.tapFormstack;
    pyPkgAnalyticsTapGit = dependencies.python.analytics.singer.tapGit;
    pyPkgAnalyticsTapJson = dependencies.python.analytics.singer.tapJson;
    pyPkgAnalyticsTapTimedoctor = dependencies.python.analytics.singer.tapTimedoctor;
    pyPkgAnalyticsTargetRedshift = dependencies.python.analytics.singer.targetRedshift;
    pyPkgFluidCLI = dependencies.python.fluidAttacks;
    pyPkgMandrill = dependencies.python.mandrill;
    pyPkgProspector = dependencies.python.prospector;
    pyPkgUrllib3 = dependencies.python.urllib3;

    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;
    srcExternalGitlabVariables = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/-/raw/6a28929bd69aa6b286354b84e211edaf70da78b4/shared-scripts/gitlab-variables.sh";
      sha256 = "13y7xd9n0859lgncljxbkgvdhx9akxflkarcv4klsn9cqz3mgr06";
    };
    srcExternalMail = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/-/raw/14cb9f1fd1b14fd024853547968f60dc35269ecf/shared-scripts/mail.py";
      sha256 = "1a7kki53qxdwfh5s6043ygnyzk0liszxn4fygzfkwx7nhsmdf6k3";
    };
    srcExternalSops = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/-/raw/3f902492c7186d22b522068a0e2920841fd90e7a/shared-scripts/sops.sh";
      sha256 = "0alm1k5dj5fvcdyygm9bk58kgpkjnzl2k7p7d5if5cw8j8bi32rb";
    };
    srcDotDotToolboxOthers = ../toolbox/others.sh;

    LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
  }
