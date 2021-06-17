{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocsDevelopment = path "/docs/src/docs/development/";
    envSrcDocsAbout = path "/docs/src/docs/about/";
    envSrcDocsSquad = path "/docs/src/docs/squad/";
    envSrcDocsMachine = path "/docs/src/docs/machine/";
    envSrcDocsCriteriaCompliance = path "/docs/src/docs/criteria/compliance/";
    envSrcDocsCriteriaRequirementsArchitecture = path "/docs/src/docs/criteria/requirements/architecture/";
    envSrcDocsCriteriaRequirementsAuthentication = path "/docs/src/docs/criteria/requirements/authentication/";
    envSrcDocsCriteriaRequirementsAuthorization = path "/docs/src/docs/criteria/requirements/authorization/";
    envSrcDocsCriteriaRequirementsCertificates = path "/docs/src/docs/criteria/requirements/certificates/";
    envSrcDocsCriteriaRequirementsCredentials = path "/docs/src/docs/criteria/requirements/credentials/";
    envSrcDocsCriteriaRequirementsCryptography = path "/docs/src/docs/criteria/requirements/cryptography/";
    envSrcDocsCriteriaRequirementsData = path "/docs/src/docs/criteria/requirements/data/";
    envSrcDocsCriteriaRequirementsDevices = path "/docs/src/docs/criteria/requirements/devices/";
    envSrcDocsCriteriaRequirementsEmails = path "/docs/src/docs/criteria/requirements/emails/";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
