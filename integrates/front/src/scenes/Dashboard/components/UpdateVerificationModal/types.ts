interface IRequestVulnVerificationResult {
  requestVulnerabilitiesVerification: {
    success: boolean;
  };
}

interface IVerifyRequestVulnResult {
  verifyVulnerabilitiesRequest: {
    success: boolean;
  };
}

export { IRequestVulnVerificationResult, IVerifyRequestVulnResult };
