let
  commonPath = "/observes/common";
  singerPath = "/observes/singer";
  std_data = root: {
    inherit root;
    env = {
      runtime = builtins.replaceStrings [ "_" ] [ "-" ] "${root}/env/runtime";
      dev = builtins.replaceStrings [ "_" ] [ "-" ] "${root}/env/development";
    };
    bin = builtins.replaceStrings [ "_" ] [ "-" ] "${root}/bin";
    src = "${root}/${baseNameOf root}";
    tests = "${root}/tests";
  };
in
{
  common = {
    paginator = "${commonPath}/paginator";
    postgresClient = "${commonPath}/postgres_client";
    purity = "${commonPath}/purity";
    singerIO = "${commonPath}/singer_io";
    utilsLogger = "${commonPath}/utils_logger";
  };
  tap = {
    announcekit = std_data "${singerPath}/tap_announcekit";
    bugsnag = std_data "${singerPath}/tap_bugsnag";
    checkly = std_data "${singerPath}/tap_checkly";
    csv = std_data "${singerPath}/tap_csv";
    delighted = std_data "${singerPath}/tap_delighted";
    dynamo = std_data "${singerPath}/tap_dynamo";
    formstack = std_data "${singerPath}/tap_formstack";
    git = std_data "${singerPath}/tap_git";
    gitlab = std_data "${singerPath}/tap_gitlab";
    json = std_data "${singerPath}/tap_json";
    mailchimp = "${singerPath}/tap_mailchimp";
    mixpanel = "${singerPath}/tap_mixpanel";
    timedoctor = "${singerPath}/tap_timedoctor";
    toe_files = "${singerPath}/tap_toe_files";
    zoho_analytics = "${singerPath}/tap_zoho_analytics";
    zoho_crm = "${singerPath}/streamer_zoho_crm";
  };
  target = {
    redshift = "${singerPath}/target_redshift";
  };
}
