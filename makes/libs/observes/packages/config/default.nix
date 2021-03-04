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
        "GitPython==3.1.13"
        "ratelimiter==1.2.0"
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "gitdb==4.0.5"
        "idna==2.10"
        "smmap==3.0.5"
        "urllib3==1.26.3"
        "uvloop==0.14.0"
      ];
    };
    local = [ ];
    nix = [
      nixPkgs.git
      nixPkgs.python38Packages.psycopg2
    ];
  };

  codeEtlDev = {
    srcPath = path "/observes/code_etl";
    python = {
      direct = mergeDeps [
        codeEtl.python.direct
        [
          "pytest-asyncio==0.14.0"
          "pytest==6.2.2"
        ]
      ];
      inherited = mergeDeps [
        codeEtl.python.inherited
        [
          "atomicwrites==1.4.0"
          "attrs==20.3.0"
          "iniconfig==1.1.1"
          "more-itertools==8.7.0"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "toml==0.10.2"
          "wcwidth==0.2.5"
        ]
      ];
    };
    local = codeEtl.local;
    nix = codeEtl.nix;
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
      ];
      inherited = [
        "aioextensions==20.8.2087641"
        "asgiref==3.2.10"
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "multidict==4.7.6"
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
  difGitlabEtlDev = {
    srcPath = path "/observes/etl/dif_gitlab_etl";
    python = {
      direct = mergeDeps [
        difGitlabEtl.python.direct
        [
          "pytest-asyncio==0.14.0"
          "pytest-timeout==1.4.2"
          "pytest==6.1.1"
        ]
      ];
      inherited = mergeDeps [
        difGitlabEtl.python.inherited
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
    local = difGitlabEtl.local;
    nix = difGitlabEtl.nix;
  };
  postgresClient = {
    srcPath = path "/observes/common/postgres_client";
    python = {
      direct = [ ];
      inherited = [ ];
    };
    local = [ ];
    nix = [
      nixPkgs.postgresql
      nixPkgs.python38Packages.psycopg2
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

  serviceBatchStability = {
    srcPath = path "/observes/services/batch_stability";
    python = {
      direct = [
        "boto3==1.17.17"
        "bugsnag==4.0.2"
      ];
      inherited = [
        "botocore==1.20.17"
        "jmespath==0.10.0"
        "python-dateutil==2.8.1"
        "s3transfer==0.3.4"
        "six==1.15.0"
        "urllib3==1.26.3"
        "WebOb==1.8.7"
      ];
    };
    local = [ ];
    nix = [ ];
  };

  serviceMigrateTables = {
    srcPath = path "/observes/services/migrate_tables";
    python = {
      direct = [
        "click==7.1.2"
      ];
      inherited = [ ];
    };
    local = [
      "postgresClient"
    ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };

  serviceTimedoctorTokens = {
    srcPath = path "/observes/services/timedoctor_tokens";
    python = {
      direct = [
        "click==7.1.2"
      ];
      inherited = [ ];
    };
    local = [ ];
    nix = [ ];
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

  streamerDynamoDB = {
    srcPath = path "/observes/singer/streamer_dynamodb";
    python = {
      direct = [
        "aioboto3==8.0.5"
        "aioextensions==20.8.2087641"
        "aiomultiprocess==0.8.0"
      ];
      inherited = [
        "aiobotocore==1.0.4"
        "aiohttp==3.7.3"
        "aioitertools==0.7.1"
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "boto3==1.12.32"
        "botocore==1.15.32"
        "chardet==3.0.4"
        "docutils==0.15.2"
        "idna==3.1"
        "jmespath==0.10.0"
        "multidict==5.1.0"
        "python-dateutil==2.8.1"
        "s3transfer==0.3.4"
        "six==1.15.0"
        "typing-extensions==3.7.4.3"
        "urllib3==1.25.11"
        "uvloop==0.15.1"
        "wrapt==1.12.1"
        "yarl==1.6.3"
      ];
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
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "idna==2.10"
        "urllib3==1.26.3"
      ];
    };
    local = [
      "postgresClient"
      "singerIO"
    ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };

  streamerZohoCrmDev = {
    srcPath = streamerZohoCrm.srcPath;
    python = {
      direct = mergeDeps [
        streamerZohoCrm.python.direct
        [
          "pytest-postgresql==2.5.2"
          "pytest==5.2.0"
        ]
      ];
      inherited = mergeDeps [
        streamerZohoCrm.python.inherited
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
    local = streamerZohoCrm.local;
    nix = streamerZohoCrm.nix;
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

  tapCsvDev = {
    srcPath = tapCsv.srcPath;
    python = {
      direct = mergeDeps [
        tapCsv.python.direct
        [
          "pytest==5.2.0"
        ]
      ];
      inherited = mergeDeps [
        tapCsv.python.inherited
        [
          "atomicwrites==1.4.0"
          "attrs==20.3.0"
          "more-itertools==8.7.0"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "wcwidth==0.2.5"
        ]
      ];
    };
    local = tapCsv.local;
    nix = tapCsv.nix;
  };

  tapFormstack = {
    srcPath = path "/observes/singer/tap_formstack";
    python = {
      direct = [
        "python-dateutil==2.8.1"
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "six==1.15.0"
        "urllib3==1.26.3"
      ];
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

  tapMailchimp = {
    srcPath = path "/observes/singer/tap_mailchimp";
    python = {
      direct = [
        "click==7.1.2"
        "mailchimp-marketing==3.0.31"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "python-dateutil==2.8.1"
        "requests==2.25.1"
        "six==1.15.0"
        "urllib3==1.26.3"
      ];
    };
    local = [
      "singerIO"
    ];
    nix = [ ];
  };

  tapMailchimpDev = {
    srcPath = tapMailchimp.srcPath;
    python = {
      direct = mergeDeps [
        tapMailchimp.python.direct
        [
          "pytest==6.2.2"
        ]
      ];
      inherited = mergeDeps [
        tapMailchimp.python.inherited
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
    local = tapMailchimp.local;
    nix = tapMailchimp.nix;
  };

  tapMixpanel = {
    srcPath = path "/observes/singer/tap_mixpanel";
    python = {
      direct = [
        "boto3==1.17.20"
        "botocore==1.20.20"
        "ratelimiter==1.2.0"
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "jmespath==0.10.0"
        "numpy==1.20.1"
        "python-dateutil==2.8.1"
        "pytz==2021.1"
        "s3transfer==0.3.4"
        "six==1.15.0"
        "urllib3==1.26.2"
      ];
    };
    local = [
      "singerIO"
    ];
    nix = [
      nixPkgs.python38Packages.pandas
    ];
  };

  tapMixpanelDev = {
    srcPath = tapMixpanel.srcPath;
    python = {
      direct = mergeDeps [
        tapMixpanel.python.direct
        [
          "pytest-freezegun==0.4.2"
          "pytest==6.2.2"
        ]
      ];
      inherited = mergeDeps [
        tapMixpanel.python.inherited
        [
          "attrs==20.3.0"
          "freezegun==1.1.0"
          "iniconfig==1.1.1"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "toml==0.10.2"
        ]
      ];
    };
    local = tapMixpanel.local;
    nix = tapMixpanel.nix;
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

  tapToeFiles = {
    srcPath = path "/observes/singer/tap_toe_files";
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
    local = [
      "postgresClient"
      "singerIO"
    ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };

  targetRedshiftDev = {
    srcPath = targetRedshift.srcPath;
    python = {
      direct = mergeDeps [
        targetRedshift.python.direct
        [
          "pytest==5.2.0"
        ]
      ];
      inherited = mergeDeps [
        targetRedshift.python.inherited
        [
          "atomicwrites==1.4.0"
          "attrs==20.3.0"
          "more-itertools==8.7.0"
          "packaging==20.9"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "wcwidth==0.2.5"
        ]
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
      ];
      inherited = [ ];
    };
    local = [ ];
    nix = [
      nixPkgs.python38Packages.psycopg2
    ];
  };
}
