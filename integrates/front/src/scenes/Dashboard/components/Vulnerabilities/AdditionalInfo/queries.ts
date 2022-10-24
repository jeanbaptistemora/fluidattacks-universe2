/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { gql } from "@apollo/client";
import type { DocumentNode } from "graphql";

const GET_VULN_ADDITIONAL_INFO: DocumentNode = gql`
  query GetVulnAdditionalInfo($canRetrieveHacker: Boolean!, $vulnId: String!) {
    vulnerability(uuid: $vulnId) {
      commitHash
      cycles
      efficacy
      hacker @include(if: $canRetrieveHacker)
      lastReattackRequester
      lastRequestedReattackDate
      lastStateDate
      lastTreatmentDate
      reportDate
      severity
      source
      stream
      treatment
      treatmentAcceptanceDate
      treatmentAssigned
      treatmentChanges
      treatmentJustification
      vulnerabilityType
    }
  }
`;

export { GET_VULN_ADDITIONAL_INFO };
