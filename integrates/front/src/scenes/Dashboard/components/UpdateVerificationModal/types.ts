interface IRequestVerificationVulnResult {
  requestVerificationVuln: {
    success: boolean;
  };
}

interface IVerifyRequestVulnResult {
  verifyRequestVulnerabilities: {
    success: boolean;
  };
}

export { IRequestVerificationVulnResult, IVerifyRequestVulnResult };
