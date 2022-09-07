/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

export type {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
  ReattackVulnerabilitiesResult,
  VerificationResult,
  VerifyVulnerabilitiesResult,
};
