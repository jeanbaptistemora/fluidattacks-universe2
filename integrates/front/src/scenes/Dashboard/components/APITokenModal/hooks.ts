import type { FormAction } from "redux-form";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { useDispatch } from "react-redux";
import { useTranslation } from "react-i18next";
import type { ApolloError, ApolloQueryResult } from "apollo-client";
import {
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
  UPDATE_ACCESS_TOKEN_MUTATION,
} from "scenes/Dashboard/components/APITokenModal/queries";
import type {
  IGetAccessTokenAttr,
  IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr,
} from "scenes/Dashboard/components/APITokenModal/types";
import type { MutationFunction, MutationResult } from "@apollo/react-common";
import { change, reset } from "redux-form";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

const useUpdateAPIToken: (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
) => readonly [MutationFunction, MutationResult<IUpdateAccessTokenAttr>] = (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
): readonly [MutationFunction, MutationResult<IUpdateAccessTokenAttr>] => {
  const { t } = useTranslation();
  const dispatch: React.Dispatch<FormAction> = useDispatch();

  // Handle mutation results
  const handleOnSuccess: (mtResult: IUpdateAccessTokenAttr) => void = (
    mtResult: IUpdateAccessTokenAttr
  ): void => {
    if (mtResult.updateAccessToken.success) {
      void refetch();
      dispatch(
        change(
          "updateAccessToken",
          "sessionJwt",
          mtResult.updateAccessToken.sessionJwt
        )
      );
      msgSuccess(
        t("updateAccessToken.successfully"),
        t("updateAccessToken.success")
      );
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Invalid Expiration Time":
          msgError(t("updateAccessToken.invalidExpTime"));
          break;
        default:
          Logger.warning("An error occurred adding access token", error);
          msgError(t("groupAlerts.errorTextsad"));
      }
    });
    dispatch(reset("updateAccessToken"));
  };

  const [updateAPIToken, mtResponse] = useMutation(
    UPDATE_ACCESS_TOKEN_MUTATION,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
    }
  );

  return [updateAPIToken, mtResponse] as const;
};

const useGetAPIToken: () => readonly [
  IGetAccessTokenAttr | undefined,
  () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
] = (): readonly [
  IGetAccessTokenAttr | undefined,
  () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
] => {
  const { t } = useTranslation();

  // Handle query results
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred getting access token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const { data, refetch } = useQuery<IGetAccessTokenAttr>(GET_ACCESS_TOKEN, {
    fetchPolicy: "network-only",
    onError: handleOnError,
  });

  return [data, refetch] as const;
};

const useInvalidateAPIToken: (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>,
  onClose: () => void
) => MutationFunction = (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>,
  onClose: () => void
): MutationFunction => {
  const { t } = useTranslation();
  const dispatch: React.Dispatch<FormAction> = useDispatch();

  // Handle mutation results
  const handleOnSuccess: (mtResult: IInvalidateAccessTokenAttr) => void = (
    mtResult: IInvalidateAccessTokenAttr
  ): void => {
    if (mtResult.invalidateAccessToken.success) {
      onClose();
      msgSuccess(
        t("updateAccessToken.delete"),
        t("updateAccessToken.invalidated")
      );
      void refetch();
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred invalidating access token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
    dispatch(reset("updateAccessToken"));
  };

  const [invalidateAPIToken] = useMutation(INVALIDATE_ACCESS_TOKEN_MUTATION, {
    onCompleted: handleOnSuccess,
    onError: handleOnError,
  });

  return invalidateAPIToken;
};

export { useUpdateAPIToken, useGetAPIToken, useInvalidateAPIToken };
