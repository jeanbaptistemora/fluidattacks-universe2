import type {
  ApolloError,
  MutationFunction,
  MutationResult,
  OperationVariables,
  QueryLazyOptions,
} from "@apollo/client";
import { useLazyQuery, useMutation } from "@apollo/client";
import type { GraphQLError } from "graphql";
import { useTranslation } from "react-i18next";

import {
  GET_FORCES_TOKEN,
  UPDATE_FORCES_TOKEN_MUTATION,
} from "scenes/Dashboard/components/APITokenForcesModal/queries";
import type {
  IGetForcesTokenAttr,
  IUpdateForcesTokenAttr,
} from "scenes/Dashboard/components/APITokenForcesModal/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const useGetAPIToken: (
  groupName: string
) => readonly [
  (options?: QueryLazyOptions<OperationVariables> | undefined) => void,
  boolean,
  IGetForcesTokenAttr | undefined,
  boolean
] = (
  groupName: string
): readonly [
  (options?: QueryLazyOptions<OperationVariables> | undefined) => void,
  boolean,
  IGetForcesTokenAttr | undefined,
  boolean
] => {
  const { t } = useTranslation();
  // Handle query results
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred getting forces token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const [getForcesApiToken, { called, data, loading }] =
    useLazyQuery<IGetForcesTokenAttr>(GET_FORCES_TOKEN, {
      fetchPolicy: "network-only",
      onError: handleOnError,
      variables: {
        groupName,
      },
    });

  return [getForcesApiToken, called, data, loading] as const;
};

const useUpdateAPIToken: () => readonly [
  MutationFunction,
  MutationResult<IUpdateForcesTokenAttr>
] = (): readonly [MutationFunction, MutationResult<IUpdateForcesTokenAttr>] => {
  const { t } = useTranslation();

  // Handle mutation results
  const handleOnSuccess: (mtResult: IUpdateForcesTokenAttr) => void = (
    mtResult: IUpdateForcesTokenAttr
  ): void => {
    if (mtResult.updateForcesAccessToken.success) {
      msgSuccess(
        t("updateForcesToken.successfully"),
        t("updateForcesToken.success")
      );
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred adding access token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const [updateAPIToken, mtResponse] = useMutation(
    UPDATE_FORCES_TOKEN_MUTATION,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
      refetchQueries: [GET_FORCES_TOKEN],
    }
  );

  return [updateAPIToken, mtResponse] as const;
};

export { useGetAPIToken, useUpdateAPIToken };
