{ nixpkgs2 }:
{
  codeEtl = {
    binName = "code-etl";
    entrypoint = "from code_etl.cli import main";
    package = nixpkgs2.codeEtl;
  };

  difGitlabEtl = {
    binName = "observes-dif-gitlab-etl";
    entrypoint = "from dif_gitlab_etl.cli import main";
    package = nixpkgs2.difGitlabEtl;
  };

  serviceBatchStability = {
    binName = "observes-service-batch-stability";
    entrypoint = "from batch_stability import main";
    package = nixpkgs2.serviceBatchStability;
  };

  serviceMigrateTables = {
    binName = "observes-service-migrate-tables";
    entrypoint = "from migrate_tables.cli import main";
    package = nixpkgs2.serviceMigrateTables;
  };

  serviceTimedoctorTokens = {
    binName = "observes-service-timedoctor-tokens";
    entrypoint = "from timedoctor_tokens import main";
    package = nixpkgs2.serviceTimedoctorTokens;
  };

  streamerDynamoDB = {
    binName = "observes-streamer-dynamodb";
    entrypoint = "from streamer_dynamodb import main";
    package = nixpkgs2.streamerDynamoDB;
  };

  streamerZohoCrm = {
    binName = "observes-streamer-zoho-crm";
    entrypoint = "from streamer_zoho_crm.cli import main";
    package = nixpkgs2.streamerZohoCrm;
  };

  tapCsv = {
    binName = "observes-tap-csv";
    entrypoint = "from tap_csv.cli import main";
    package = nixpkgs2.tapCsv;
  };

  tapFormstack = {
    binName = "observes-tap-formstack";
    entrypoint = "from tap_formstack import main";
    package = nixpkgs2.tapFormstack;
  };

  tapMailchimp = {
    binName = "observes-tap-mailchimp";
    entrypoint = "from tap_mailchimp.cli import main";
    package = nixpkgs2.tapMailchimp;
  };

  tapMixpanel = {
    binName = "observes-tap-mixpanel";
    entrypoint = "from tap_mixpanel import main";
    package = nixpkgs2.tapMixpanel;
  };

  tapTimedoctor = {
    binName = "observes-tap-timedoctor";
    entrypoint = "from tap_timedoctor import main";
    package = nixpkgs2.tapTimedoctor;
  };

  tapToeFiles = {
    binName = "observes-tap-toe-files";
    entrypoint = "from tap_toe_files import main";
    package = nixpkgs2.tapToeFiles;
  };

  updateSyncDate = {
    binName = "observes-update-sync-date";
    entrypoint = "from update_s3_last_sync_date.cli import main";
    package = nixpkgs2.updateSyncDate;
  };
}
