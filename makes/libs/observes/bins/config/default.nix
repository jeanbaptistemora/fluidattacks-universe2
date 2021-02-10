{ observesPkgs }:
{
  codeEtl = {
    binName = "code-etl";
    entrypoint = "from code_etl.cli import main";
    package = observesPkgs.codeEtl;
  };

  difGitlabEtl = {
    binName = "observes-dif-gitlab-etl";
    entrypoint = "from dif_gitlab_etl.cli import main";
    package = observesPkgs.difGitlabEtl;
  };

  streamerZohoCrm = {
    binName = "observes-streamer-zoho-crm";
    entrypoint = "from streamer_zoho_crm.cli import main";
    package = observesPkgs.streamerZohoCrm;
  };

  tapCsv = {
    binName = "observes-tap-csv";
    entrypoint = "from tap_csv.cli import main";
    package = observesPkgs.tapCsv;
  };

  tapFormstack = {
    binName = "observes-tap-formstack";
    entrypoint = "from tap_formstack import main";
    package = observesPkgs.tapFormstack;
  };

  updateSyncDate = {
    binName = "observes-update-sync-date";
    entrypoint = "from update_s3_last_sync_date.cli import main";
    package = observesPkgs.updateSyncDate;
  };
}
