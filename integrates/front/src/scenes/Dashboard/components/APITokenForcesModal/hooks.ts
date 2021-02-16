import type { ApolloError } from "apollo-client";
import { GET_FORCES_TOKEN } from "scenes/Dashboard/components/APITokenForcesModal/queries";
import type { GraphQLError } from "graphql";
import type { IGetForcesTokenAttr } from "scenes/Dashboard/components/APITokenForcesModal/types";
import { Logger } from "utils/logger";
import type { OperationVariables } from "@apollo/react-common";
import type { QueryLazyOptions } from "@apollo/react-hooks";
import { msgError } from "utils/notifications";
import { useLazyQuery } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";

const useGetAPIToken: (
  groupName: string
) => readonly [
  (options?: QueryLazyOptions<OperationVariables> | undefined) => void,
  IGetForcesTokenAttr | undefined
] = (
  groupName: string
): readonly [
  (options?: QueryLazyOptions<OperationVariables> | undefined) => void,
  IGetForcesTokenAttr | undefined
] => {
  const { t } = useTranslation();
  // Handle query results
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred getting forces token", error);
      msgError(t("group_alerts.error_textsad"));
    });
  };

  const [getForcesApiToken, { data }] = useLazyQuery<IGetForcesTokenAttr>(
    GET_FORCES_TOKEN,
    {
      fetchPolicy: "network-only",
      onError: handleOnError,
      variables: {
        groupName: groupName,
      },
    }
  );

  return [getForcesApiToken, data] as const;
};

export { useGetAPIToken };
