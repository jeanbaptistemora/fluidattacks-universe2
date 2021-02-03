{ nixPkgs, path }:
let
  nixUtils = import (path "/makes/utils/nix") path nixPkgs;
  sort = nixUtils.sortCaseless;
  verifySort = list:
    if (sort list == list)
    then list
    else abort "Python requirements must be sorted in this order: ${builtins.toJSON (sort list)}";
  mergeDeps = lists: sort (
    builtins.foldl' (a: b: a ++ b) [ ] (builtins.map verifySort lists)
  );
in
rec {
  codeEtl = {
    srcPath = path "/observes/code_etl";
    python = {
      direct = [
        "aioextensions==20.9.2315218"
        "click==7.1.2"
        "psycopg2==2.8.4"
        "pytest==5.2.0"
        "ratelimiter==1.2.0"
        "requests==2.25.1"
      ];
      inherited = [
        "atomicwrites==1.4.0"
        "attrs==20.3.0"
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "ddt==1.2.2"
        "gitdb==4.0.2"
        "GitPython==3.1.0"
        "idna==2.10"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "smmap==3.0.1"
        "urllib3==1.26.3"
        "uvloop==0.14.0"
        "wcwidth==0.2.5"
      ];
    };
    local = [ ];
    nix = [
      nixPkgs.git
      nixPkgs.python38Packages.psycopg2
    ];
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
        "pytest-asyncio==0.14.0"
        "pytest-timeout==1.4.2"
        "pytest==6.1.1"
      ];
      inherited = [
        "aioextensions==20.8.2087641"
        "asgiref==3.2.10"
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "iniconfig==1.1.1"
        "multidict==4.7.6"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "toml==0.10.2"
        "uvloop==0.14.0"
        "yarl==1.6.3"
      ];
    };
    local = [
      "streamerGitlab"
    ];
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
    ];
  };

  postgresClientDev = {
    srcPath = postgresClient.srcPath;
    python = {
      direct = mergeDeps [
        postgresClient.python.direct
        [
          "pytest-postgresql==2.5.2"
          "pytest-timeout==1.4.2"
          "pytest==5.2.0"
        ]
      ];
      inherited = mergeDeps [
        postgresClient.python.inherited
        [
          "atomicwrites==1.4.0"
          "attrs==20.3.0"
          "mirakuru==2.3.0"
          "more-itertools==8.6.0"
          "packaging==20.9"
          "pluggy==0.13.1"
          "port-for==0.4"
          "psutil==5.8.0"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "wcwidth==0.2.5"
        ]
      ];
    };
    local = postgresClient.local;
    nix = postgresClient.nix;
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

  singerIOdev = {
    srcPath = singerIO.srcPath;
    python = {
      direct = mergeDeps [
        singerIO.python.direct
        [
          "pytest==6.1.2"
        ]
      ];
      inherited = mergeDeps [
        singerIO.python.inherited
        [
          "attrs==20.3.0"
          "iniconfig==1.1.1"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "toml==0.10.2"
        ]
      ];
    };
    local = singerIO.local;
    nix = singerIO.nix;
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
      direct = [
        "aioextensions==20.8.2087641"
        "aiohttp==3.6.2"
        "asgiref==3.2.10"
      ];
      inherited = [
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "multidict==4.7.6"
        "uvloop==0.14.0"
        "yarl==1.6.3"
      ];
    };
    local = [ ];
    nix = [ ];
  };

  streamerGitlabDev = {
    srcPath = streamerGitlab.srcPath;
    python = {
      direct = mergeDeps [
        streamerGitlab.python.direct
        [
          "pytest-asyncio==0.14.0"
          "pytest==6.1.1"
        ]
      ];
      inherited = mergeDeps [
        streamerGitlab.python.inherited
        [
          "iniconfig==1.1.1"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "toml==0.10.2"
        ]
      ];
    };
    local = streamerGitlab.local;
    nix = streamerGitlab.nix;
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
        "atomicwrites==1.4.0"
        "attrs==20.3.0"
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "idna==2.10"
        "mirakuru==2.3.0"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pluggy==0.13.1"
        "port-for==0.4"
        "psutil==5.8.0"
        "psycopg2==2.8.4"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "pytest-postgresql==2.5.2"
        "pytest==5.2.0"
        "urllib3==1.26.2"
        "wcwidth==0.2.5"
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
      direct = [
        "click==7.1.2"
      ];
      inherited = [ ];
    };
    local = [
      "singerIO"
    ];
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
      inherited = [
        "atomicwrites==1.4.0"
        "attrs==20.3.0"
        "mirakuru==2.3.0"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pluggy==0.13.1"
        "port-for==0.4"
        "psutil==5.8.0"
        "psycopg2==2.8.4"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "pytest-postgresql==2.5.2"
        "pytest==5.2.0"
        "wcwidth==0.2.5"
      ];
    };
    local = [
      "postgresClient"
      "singerIO"
    ];
    nix = [ ];
  };

  updateSyncDate = {
    srcPath = path "/observes/services/update_s3_last_sync_date";
    python = {
      direct = [
        "click==7.1.2"
        "psycopg2==2.8.4"
      ];
      inherited = [ ];
    };
    local = [ ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };
}
