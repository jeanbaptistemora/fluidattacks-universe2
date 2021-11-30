let
  commonPath = "/observes/common";
  singerPath = "/observes/singer";
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
    announcekit = "${singerPath}/tap_announcekit";
    bugsnag = "${singerPath}/tap_bugsnag";
    checkly = "${singerPath}/tap_checkly";
    csv = "${singerPath}/tap_csv";
    delighted = "${singerPath}/tap_delighted";
    dynamo = "${singerPath}/tap_dynamo";
    formstack = "${singerPath}/tap_formstack";
    git = "${singerPath}/tap_git";
    gitlab = "${singerPath}/tap_gitlab";
    json = "${singerPath}/tap_json";
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
