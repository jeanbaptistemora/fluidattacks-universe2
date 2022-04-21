let
  commonPath = "/observes/common";
  singerPath = "/observes/singer";
  etlsPath = "/observes/etl";
  underscore_pkg = root: builtins.replaceStrings ["-"] ["_"] (baseNameOf root);
  std_data = root: {
    root = "${root}/src";
    env = {
      runtime = "${root}/env/runtime";
      dev = "${root}/env/development";
    };
    bin = "${root}/bin";
    src = "${root}/src/${underscore_pkg root}";
    tests = "${root}/src/tests";
    lint = "${root}/lint";
    test = "${root}/test";
  };
  new_std = root: {
    inherit root;
    src = "${root}/${underscore_pkg root}";
    check = {
      arch = "${root}/check/arch";
      types = "${root}/check/types";
    };
    bin = "${root}/bin";
    env = {
      runtime = "${root}/env/runtime";
      dev = "${root}/env/dev";
    };
    lint = "${root}/lint";
    test = "${root}/test";
  };
in {
  service = {
    db_migration =
      (std_data "/observes/service/db-migration")
      // {
        root = "/observes/service/db-migration/src";
      };
    scheduler =
      (std_data "/observes/service/jobs-scheduler")
      // {
        root = "/observes/service/jobs-scheduler/src";
      };
  };
  etl = {
    dynamo =
      (new_std "${etlsPath}/dynamo_etl_conf")
      // {
        env = {
          runtime = "/observes/etl/dynamo/conf/env/runtime";
          dev = "/observes/etl/dynamo/conf/env/dev";
        };
      };
    code =
      (new_std "${etlsPath}/code")
      // {
        root = "/observes/code_etl";
      };
  };
  common = {
    paginator = "${commonPath}/paginator";
    postgresClient = "${commonPath}/postgres-client/src";
    purity = "${commonPath}/purity";
    singer_io =
      std_data "${commonPath}/singer-io"
      // {
        env2.dev = "${commonPath}/singer-io/env2/dev";
      };
    utils_logger =
      std_data "${commonPath}/utils-logger"
      // {
        new_env.dev = "${commonPath}/utils-logger/new-env/dev";
      };
  };
  tap = {
    announcekit = std_data "${singerPath}/tap-announcekit";
    bugsnag = std_data "${singerPath}/tap-bugsnag";
    checkly = new_std "${singerPath}/tap-checkly";
    csv = std_data "${singerPath}/tap-csv";
    delighted = std_data "${singerPath}/tap-delighted";
    dynamo = std_data "${singerPath}/tap-dynamo";
    formstack = std_data "${singerPath}/tap-formstack";
    git = std_data "${singerPath}/tap-git";
    gitlab = std_data "${singerPath}/tap-gitlab";
    json = std_data "${singerPath}/tap-json";
    mailchimp = std_data "${singerPath}/tap-mailchimp";
    mixpanel = std_data "${singerPath}/tap-mixpanel";
    timedoctor = std_data "${singerPath}/tap-timedoctor";
    zoho_analytics = std_data "${singerPath}/tap-zoho-analytics";
    zoho_crm = std_data "${singerPath}/tap-zoho-crm";
  };
  target = {
    redshift = std_data "${singerPath}/target-redshift";
  };
}
