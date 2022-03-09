let
  commonPath = "/observes/common";
  singerPath = "/observes/singer";
  etlsPath = "/observes/etl";
  std_data = root: {
    inherit root;
    env = {
      runtime = builtins.replaceStrings ["_"] ["-"] "${root}/env/runtime";
      dev = builtins.replaceStrings ["_"] ["-"] "${root}/env/development";
    };
    bin = builtins.replaceStrings ["_"] ["-"] "${root}/bin";
    src = "${root}/${baseNameOf root}";
    tests = "${root}/tests";
  };
  streamer_zoho_crm = std_data "${singerPath}/streamer_zoho_crm";
in {
  service = {
    db_migration =
      (std_data "/observes/service/db_migration")
      // {
        root = "/observes/services/db_migration";
      };
  };
  etl = {
    dynamo =
      (std_data "${etlsPath}/dynamo_etl_conf")
      // {
        env = {
          runtime = "/observes/etl/dynamo/conf/env/runtime";
          dev = "/observes/etl/dynamo/conf/env/development";
        };
      };
  };
  common = {
    paginator = "${commonPath}/paginator";
    postgresClient = "${commonPath}/postgres_client";
    purity = "${commonPath}/purity";
    singerIO = "${commonPath}/singer_io";
    utils_logger =
      std_data "${commonPath}/utils_logger"
      // {
        new_env.dev = builtins.replaceStrings ["_"] ["-"] "${commonPath}/utils_logger/new_env/dev";
      };
  };
  tap = {
    announcekit = std_data "${singerPath}/tap_announcekit";
    bugsnag = std_data "${singerPath}/tap_bugsnag";
    checkly = std_data "${singerPath}/tap_checkly";
    csv = std_data "${singerPath}/tap_csv";
    delighted = std_data "${singerPath}/tap_delighted";
    dynamo = std_data "${singerPath}/tap_dynamo";
    streamer_dynamodb = std_data "${singerPath}/streamer_dynamodb";
    formstack = std_data "${singerPath}/tap_formstack";
    git = std_data "${singerPath}/tap_git";
    gitlab = std_data "${singerPath}/tap_gitlab";
    json = std_data "${singerPath}/tap_json";
    mailchimp = std_data "${singerPath}/tap_mailchimp";
    mixpanel = std_data "${singerPath}/tap_mixpanel";
    timedoctor = std_data "${singerPath}/tap_timedoctor";
    zoho_analytics = std_data "${singerPath}/tap_zoho_analytics";
    zoho_crm =
      std_data "${singerPath}/tap_zoho_crm"
      // {
        root = streamer_zoho_crm.root;
        src = streamer_zoho_crm.src;
        tests = streamer_zoho_crm.tests;
      };
  };
  target = {
    redshift = std_data "${singerPath}/target_redshift";
  };
}
