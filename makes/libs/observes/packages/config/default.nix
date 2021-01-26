{ nixPkgs, path }:
{
  code = {
    srcPath = path "/observes/code";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  difDynamoEtl = {
    srcPath = path "/observes/etl/dif_dynamo_etl";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  difGitlabEtl = {
    srcPath = path "/observes/etl/dif_gitlab_etl";
    python = {
      direct = [
        "aiohttp==3.6.2"
        "click==7.1.2"
        "nest-asyncio==1.4.1"
        "psycopg2==2.8.4"
      ];
      inherited = [
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "multidict==4.7.6"
        "yarl==1.6.3"
      ];
    };
    local = [ ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };
  postgresClient = {
    srcPath = path "/observes/common/postgres_client";
    python = {
      direct = [
        "psycopg2==2.8.4"
      ];
      inherited = [ ];
    };
    local = [ ];
    nix = [
      nixPkgs.postgresql
      nixPkgs.python38Packages.psycopg2
    ];
  };
  singerIO = {
    srcPath = path "/observes/common/singer_io";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  streamerDynamoDb = {
    srcPath = path "/observes/singer/streamer_dynamodb";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  streamerGitlab = {
    srcPath = path "/observes/singer/streamer_gitlab";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  streamerZohoCrm = {
    srcPath = path "/observes/singer/streamer_zoho_crm";
    python = {
      direct = [
        "click==7.1.2"
        "ratelimiter==1.2.0"
        "requests==2.25.0"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "idna==2.10"
        "psycopg2==2.8.4"
        "urllib3==1.26.2"
      ];
    };
    local = [
      "postgresClient"
      "singerIO"
    ];
    nix = [ ];
  };
  tapCsv = {
    srcPath = path "/observes/singer/tap_csv";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  tapFormstack = {
    srcPath = path "/observes/singer/tap_formstack";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  tapGit = {
    srcPath = path "/observes/singer/tap_git";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  tapJson = {
    srcPath = path "/observes/singer/tap_json";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  tapMixpanel = {
    srcPath = path "/observes/singer/tap_mixpanel";
    python = {
      direct = [
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "urllib3==1.26.2"
      ];
    };
    local = [
      "singerIO"
    ];
    nix = [ ];
  };
  tapTimedoctor = {
    srcPath = path "/observes/singer/tap_timedoctor";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
  targetRedshift = {
    srcPath = path "/observes/singer/target_redshift_2";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
  };
}
