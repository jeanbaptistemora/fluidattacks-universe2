import type { ApolloError } from "apollo-client";
import type { FormAction } from "redux-form";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import type { QueryLazyOptions } from "@apollo/react-hooks";
import { useDispatch } from "react-redux";
import { useTranslation } from "react-i18next";
import {
  GET_FORCES_TOKEN,
  UPDATE_FORCES_TOKEN_MUTATION,
} from "scenes/Dashboard/components/APITokenForcesModal/queries";
import type {
  IGetForcesTokenAttr,
  IUpdateForcesTokenAttr,
} from "scenes/Dashboard/components/APITokenForcesModal/types";
import type {
  MutationFunction,
  MutationResult,
  OperationVariables,
} from "@apollo/react-common";
import { change, reset } from "redux-form";
import { msgError, msgSuccess } from "utils/notifications";
import { useLazyQuery, useMutation } from "@apollo/react-hooks";

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

  const [
    getForcesApiToken,
    { called, data, loading },
  ] = useLazyQuery<IGetForcesTokenAttr>(GET_FORCES_TOKEN, {
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
  const dispatch: React.Dispatch<FormAction> = useDispatch();

  // Handle mutation results
  const handleOnSuccess: (mtResult: IUpdateForcesTokenAttr) => void = (
    mtResult: IUpdateForcesTokenAttr
  ): void => {
    if (mtResult.updateForcesAccessToken.success) {
      dispatch(
        change(
          "updateForcesAccessToken",
          "sessionJwt",
          mtResult.updateForcesAccessToken.sessionJwt
        )
      );
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
    dispatch(reset("updateAccessToken"));
  };

  const [updateAPIToken, mtResponse] = useMutation(
    UPDATE_FORCES_TOKEN_MUTATION,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
    }
  );

  return [updateAPIToken, mtResponse] as const;
};

export { useGetAPIToken, useUpdateAPIToken };
