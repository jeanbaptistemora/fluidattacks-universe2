import { GraphQLError } from "graphql";
import { Logger } from "../../../../utils/logger";
import { useDispatch } from "react-redux";
import { useTranslation } from "react-i18next";
import { ApolloError, ApolloQueryResult } from "apollo-client";
import { FormAction, change, reset } from "redux-form";
import {
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
  UPDATE_ACCESS_TOKEN_MUTATION,
} from "./queries";
import {
  IGetAccessTokenAttr,
  IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr,
} from "./types";
import { MutationFunction, MutationResult } from "@apollo/react-common";
import { msgError, msgSuccess } from "../../../../utils/notifications";
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
        t("update_access_token.successfully"),
        t("update_access_token.success")
      );
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Invalid Expiration Time":
          msgError(t("update_access_token.invalid_exp_time"));
          break;
        default:
          Logger.warning("An error occurred adding access token", error);
          msgError(t("group_alerts.error_textsad"));
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
      msgError(t("group_alerts.error_textsad"));
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
        t("update_access_token.delete"),
        t("update_access_token.invalidated")
      );
      void refetch();
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred invalidating access token", error);
      msgError(t("group_alerts.error_textsad"));
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
