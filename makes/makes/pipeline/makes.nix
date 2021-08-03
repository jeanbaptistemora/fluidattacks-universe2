{ gitlabCi
, ...
}:
let
  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|makes)";

  gitlabOnlyMaster = [
    gitlabCi.rules.branchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    makes = {
      gitlabPath = "/makes/makes/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/makesCi";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesCompute";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesDns";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesFoss";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesSecrets";
          gitlabExtra = gitlabDeployInfra;
        }
      ];
    };
  };
}
