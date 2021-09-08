let
  commonPath = "/observes/common";
  singerPath = "/observes/singer";
in
{
  common = {
    paginator = "${commonPath}/paginator";
    postgresClient = "${commonPath}/postgres_client";
    singerIO = "${commonPath}/singer_io";
    utilsLogger = "${commonPath}/utils_logger";
  };
  taps = {
    announcekit = "${singerPath}/tap_announcekit";
  };
}
