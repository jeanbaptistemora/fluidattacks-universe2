interface IRequestVerificationVulnResult {
  requestVerificationVulnerabilities: {
    success: boolean;
  };
}

interface IVerifyRequestVulnResult {
  verifyRequestVulnerabilities: {
    success: boolean;
  };
}

export { IRequestVerificationVulnResult, IVerifyRequestVulnResult };
