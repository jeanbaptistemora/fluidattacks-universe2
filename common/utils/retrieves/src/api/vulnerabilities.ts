import type { ApolloError } from "@apollo/client";

import { REQUEST_VULNERABILITIES_VERIFICATION } from "../queries";
import { API_CLIENT } from "../utils/apollo";

interface IRequestReattackData {
  requestVulnerabilitiesVerification: { success: boolean; message?: string };
}

interface IRequestReattackRespose {
  data: IRequestReattackData;
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

export { requestReattack };
