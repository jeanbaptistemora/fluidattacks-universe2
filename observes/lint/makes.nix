# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeSearchPaths,
  outputs,
  projectPath,
  ...
}: let
  extract_roots = target: builtins.map (key: (builtins.getAttr key target).root) (builtins.attrNames target);
in {
  lintPython = {
    imports = {
      observesArch = {
        config = "/observes/architecture/setup.imports.cfg";
        searchPaths.source = [
          (makeSearchPaths {
            pythonPackage = builtins.map projectPath (
              [
                "/observes/code_etl"
                "/observes/common/paginator"
                "/observes/common/singer-io/src"
                "/observes/common/utils-logger/src"
                "/observes/common/postgres-client/src"
                "/observes/common/purity"
                "/observes/singer/tap-zoho-crm/src"
              ]
              ++ [
                inputs.observesIndex.service.scheduler.root
                inputs.observesIndex.service.batch_stability.root
                inputs.observesIndex.service.job_last_success.root
              ]
              ++ (
                extract_roots inputs.observesIndex.tap
              )
              ++ (
                extract_roots inputs.observesIndex.target
              )
            );
          })
        ];
        src = "/observes/architecture";
      };
      observesCommonPaginator = {
        config = "/observes/common/paginator/paginator/setup.imports.cfg";
        src = "/observes/common/paginator";
      };
      observesCommonPostgresClient = {
        config = "/observes/common/postgres-client/src/setup.imports.cfg";
        src = "/observes/common/postgres-client/src";
      };
      observesCommonPurity = {
        config = "/observes/common/purity/purity/setup.imports.cfg";
        src = "/observes/common/purity";
      };
      observesCommonSingerIo = {
        config = "/observes/common/singer-io/src/setup.imports.cfg";
        src = "/observes/common/singer-io/src";
      };
      observesTapAnnounceKit = {
        config = "${inputs.observesIndex.tap.announcekit.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.announcekit.root;
      };
      observesTapBugsnag = {
        config = "${inputs.observesIndex.tap.bugsnag.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.bugsnag.root;
      };
      observesTapCsv = {
        config = "${inputs.observesIndex.tap.csv.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.csv.root;
      };
      observesTapDelighted = {
        config = "${inputs.observesIndex.tap.delighted.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.delighted.root;
      };
      observesTapFormstack = {
        config = "${inputs.observesIndex.tap.formstack.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.formstack.root;
      };
      observesTapJson = {
        config = "${inputs.observesIndex.tap.json.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.json.root;
      };
      observesTapMailchimp = {
        config = "${inputs.observesIndex.tap.mailchimp.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.mailchimp.root;
      };
      observesTapMatomo = {
        config = "${inputs.observesIndex.tap.matomo.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.matomo.root;
      };
      observesTapMixpanel = {
        config = "${inputs.observesIndex.tap.mixpanel.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.mixpanel.root;
      };
      observesTapTimedoctor = {
        config = "${inputs.observesIndex.tap.timedoctor.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.timedoctor.root;
      };
    };
    modules = {
      observesCommonPaginator = {
        searchPaths.source = [
          outputs."/observes/common/paginator/env/development"
          outputs."/observes/common/paginator/env/type-stubs"
        ];
        mypyVersion = "0.971";
        python = "3.8";
        src = "/observes/common/paginator/paginator";
      };
      observesCommonPostgresClient = {
        searchPaths.source = [
          outputs."/observes/common/postgres-client/env/development"
          outputs."/observes/common/postgres-client/env/type-stubs"
        ];
        mypyVersion = "0.971";
        python = "3.8";
        src = "/observes/common/postgres-client/src/postgres_client";
      };
      observesCommonPurity = {
        searchPaths.source = [
          outputs."/observes/common/purity/env/runtime"
        ];
        python = "3.8";
        src = "/observes/common/purity/purity";
      };
      observesCommonPurityTests = {
        searchPaths.source = [
          outputs."/observes/common/purity/env/runtime"
        ];
        python = "3.8";
        src = "/observes/common/purity/tests";
      };
      observesCommonPostgresClientTests = {
        searchPaths.source = [
          outputs."/observes/common/postgres-client/env/development"
          outputs."/observes/common/postgres-client/env/type-stubs"
        ];
        mypyVersion = "0.971";
        python = "3.8";
        src = "/observes/common/postgres-client/src/tests";
      };
      observesCommonSingerIo = {
        searchPaths.source = [
          outputs."/observes/common/singer-io/env/development"
        ];
        python = "3.8";
        src = "/observes/common/singer-io/src/singer_io";
      };
      observesCommonSingerIoTests = {
        searchPaths.source = [
          outputs."/observes/common/singer-io/env/development"
        ];
        python = "3.8";
        src = "/observes/common/singer-io/src/tests";
      };
      observesServiceMigrateTables = {
        searchPaths.source = [
          outputs."/observes/service/migrate-tables/env/runtime"
        ];
        python = "3.8";
        src = "/observes/service/migrate-tables/src/migrate_tables";
      };
      observesStreamerZohoCrm = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.zoho_crm.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.zoho_crm.src;
      };
      observesStreamerZohoCrmTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.zoho_crm.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.zoho_crm.tests;
      };
      observesTapAnnounceKit = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.announcekit.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.announcekit.src;
      };
      observesTapAnnounceKitTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.announcekit.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.announcekit.tests;
      };
      observesTapBugsnag = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.bugsnag.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.bugsnag.src;
      };
      observesTapCsv = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.csv.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.csv.src;
      };
      observesTapCsvTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.csv.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.csv.tests;
      };
      observesTapDelighted = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.delighted.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.delighted.src;
      };
      observesTapFormstack = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.formstack.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.formstack.src;
      };
      observesTapJson = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.json.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.json.src;
      };
      observesTapMailchimp = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mailchimp.src;
      };
      observesTapMailchimpTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mailchimp.tests;
      };
      observesTapMatomo = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.matomo.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.matomo.src;
      };
      observesTapMixpanel = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mixpanel.src;
      };
      observesTapMixpanelTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mixpanel.tests;
      };
      observesTapTimedoctor = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.timedoctor.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.timedoctor.src;
      };
      observesTargetRedshift = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.target.redshift.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.target.redshift.src;
      };
    };
  };
}
