import type { ExecutionResult } from "graphql";

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

type ReattackVulnerabilitiesResult =
  ExecutionResult<IRequestVulnVerificationResult>;
type VerifyVulnerabilitiesResult = ExecutionResult<IVerifyRequestVulnResult>;

type VerificationResult =
  | ReattackVulnerabilitiesResult[]
  | VerifyVulnerabilitiesResult[];

export {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
  ReattackVulnerabilitiesResult,
  VerificationResult,
  VerifyVulnerabilitiesResult,
};
