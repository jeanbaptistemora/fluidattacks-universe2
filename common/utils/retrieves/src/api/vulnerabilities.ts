import type { ApolloError } from "@apollo/client";

import {
  ACCEPT_VULNERABILITY_TEMPORARY,
  REQUEST_VULNERABILITIES_VERIFICATION,
} from "../queries";
import { API_CLIENT } from "../utils/apollo";

interface IRequestReattackData {
  requestVulnerabilitiesVerification: { success: boolean; message?: string };
}

interface IRequestReattackRespose {
  data: IRequestReattackData;
}
interface IAcceptVulnerabilityData {
  updateVulnerabilitiesTreatment: { success: boolean; message?: string };
}

interface IAcceptVulnerabilityResponse {
  data: IAcceptVulnerabilityData;
}

const requestReattack = async (
  findingId: string,
  justification: string,
  vulnerabilities: string[]
): Promise<IRequestReattackData> => {
  const result: IRequestReattackData = (
    await API_CLIENT.mutate({
      mutation: REQUEST_VULNERABILITIES_VERIFICATION,
      variables: {
        findingId,
        justification,
        vulnerabilities,
      },
    }).catch((err: ApolloError): IRequestReattackRespose => {
      return {
        data: {
          requestVulnerabilitiesVerification: {
            message: err.message,
            success: false,
          },
        },
      };
    })
  ).data;

  return result;
};

const acceptVulnerabilityTemporary = async (
  findingId: string,
  vulnerabilityId: string,
  acceptanceDate: string,
  justification: string,
  treatment: string
): Promise<IAcceptVulnerabilityData> => {
  const result: IAcceptVulnerabilityData = (
    await API_CLIENT.mutate({
      mutation: ACCEPT_VULNERABILITY_TEMPORARY,
      variables: {
        acceptanceDate,
        findingId,
        justification,
        treatment,
        vulnerabilityId,
      },
    }).catch((err: ApolloError): IAcceptVulnerabilityResponse => {
      return {
        data: {
          updateVulnerabilitiesTreatment: {
            message: err.message,
            success: false,
          },
        },
      };
    })
  ).data;

  return result;
};

export { requestReattack, acceptVulnerabilityTemporary };
export type { IAcceptVulnerabilityData };
