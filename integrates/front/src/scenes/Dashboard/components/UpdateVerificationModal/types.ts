interface IRequestVerificationVulnResult {
  requestVerificationVulnerabilities: {
    success: boolean;
  };
}

interface IVerifyRequestVulnResult {
  verifyVulnerabilitiesRequest: {
    success: boolean;
  };
}

export { IRequestVerificationVulnResult, IVerifyRequestVulnResult };
