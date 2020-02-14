pkgs:

let
  legacy.kubernetes-helm =
    let
      _pkgs = import ../pkgs/import-src.nix {
        repo = "https://github.com/NixOS/nixpkgs";
        commit = "77cbf0db0ac5dc065969d44aef2cf81776d11228";
        digest = "0lnqqbvb3dv2gmi2dgmqlxlfhb9hvj19llw5jcfd7nc02yqlk1k7";
      };
    in
      _pkgs.kubernetes-helm;

  modules.build.pythonPackage = import ../modules/builders/python-package pkgs;
  modules.build.pythonPackageLocal = import ../modules/builders/python-package-local pkgs;
  modules.env.python = import ../modules/environments/python pkgs;
in rec {
    all = with pkgs; [
      aws-iam-authenticator
      awscli
      bash
      cacert
      coreutils
      curl
      docker
      envsubst
      git
      jq
      kubectl
      legacy.kubernetes-helm
      modules.env.python
      nix
      nix-linter
      nss
      openssl
      python.analytics.singer.streamerInfrastructure
      python.analytics.singer.streamerIntercom
      python.analytics.singer.streamerMandrill
      python.analytics.singer.streamerPcap
      python.analytics.singer.streamerRingcentral
      python.analytics.singer.tapAwsdynamodb
      python.analytics.singer.tapCsv
      python.analytics.singer.tapCurrrencyconverterapi
      python.analytics.singer.tapFormstack
      python.analytics.singer.tapGit
      python.analytics.singer.tapJson
      python.analytics.singer.tapTimedoctor
      python.analytics.singer.targetRedshift
      python.mandrill
      python.prospector
      shellcheck
      sops
      terraform
      tflint
      which
    ];

    python.analytics.singer.streamerInfrastructure =
      modules.build.pythonPackageLocal ../../analytics/singer/streamer_infrastructure;

    python.analytics.singer.streamerIntercom =
      modules.build.pythonPackageLocal ../../analytics/singer/streamer_intercom;

    python.analytics.singer.streamerMandrill =
      modules.build.pythonPackageLocal ../../analytics/singer/streamer_mandrill;

    python.analytics.singer.streamerPcap =
      modules.build.pythonPackageLocal ../../analytics/singer/streamer_pcap;

    python.analytics.singer.streamerRingcentral =
      modules.build.pythonPackageLocal ../../analytics/singer/streamer_ringcentral;

    python.analytics.singer.tapAwsdynamodb =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_awsdynamodb;

    python.analytics.singer.tapCsv =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_csv;

    python.analytics.singer.tapCurrrencyconverterapi =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_currencyconverterapi;

    python.analytics.singer.tapFormstack =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_formstack;

    python.analytics.singer.tapGit =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_git;

    python.analytics.singer.tapJson =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_json;

    python.analytics.singer.tapTimedoctor =
      modules.build.pythonPackageLocal ../../analytics/singer/tap_timedoctor;

    python.analytics.singer.targetRedshift =
      modules.build.pythonPackageLocal ../../analytics/singer/target_redshift;

    python.mandrill =
      modules.build.pythonPackage "mandrill-really-maintained==1.2.4";

    python.prospector =
      modules.build.pythonPackage "prospector[with_everything]==1.2.0";
  }
