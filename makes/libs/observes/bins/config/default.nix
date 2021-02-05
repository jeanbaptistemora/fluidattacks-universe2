{ observesPkgs }:
{
  codeEtl = {
    binName = "code-etl";
    entrypoint = "from code_etl.cli import main";
    package = observesPkgs.codeEtl;
  };

  tapFormstack = {
    binName = "observes-tap-formstack";
    entrypoint = "from tap_formstack import main";
    package = observesPkgs.tapFormstack;
  };

  updateSyncDate = {
    binName = "update-sync-date";
    entrypoint = "from update_s3_last_sync_date.cli import main";
    package = observesPkgs.updateSyncDate;
  };
}
