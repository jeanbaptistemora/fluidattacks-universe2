import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import { IUpdateAccessTokenAttr } from "./types";
import { Logger } from "../../../../utils/logger";
import React from "react";
import { UPDATE_ACCESS_TOKEN_MUTATION } from "./queries";
import _ from "lodash";
import store from "../../../../store";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import { MutationFunction, MutationResult } from "@apollo/react-common";
import { change, reset } from "redux-form";
import { msgError, msgSuccess } from "../../../../utils/notifications";

export const useUpdateAPIToken: () => {
  canSubmit: [boolean, React.Dispatch<boolean>];
  canSelectDate: [boolean, React.Dispatch<boolean>];
  mtResult: [MutationFunction, MutationResult<IUpdateAccessTokenAttr>];
} = (): {
  canSubmit: [boolean, React.Dispatch<boolean>];
  canSelectDate: [boolean, React.Dispatch<boolean>];
  mtResult: [MutationFunction, MutationResult<IUpdateAccessTokenAttr>];
} => {
  const { t } = useTranslation();

  //  Handle user actions
  const [canSubmit, setCanSubmit] = React.useState(false);
  const [canSelectDate, setCanSelectDate] = React.useState(true);

  // Handle mutation results
  const handleOnSuccess: (mtResult: IUpdateAccessTokenAttr) => void = (
    mtResult: IUpdateAccessTokenAttr
  ): void => {
    if (!_.isUndefined(mtResult) && mtResult.updateAccessToken.success) {
      setCanSubmit(true);
      setCanSelectDate(false);
      store.dispatch(
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
    store.dispatch(reset("updateAccessToken"));
  };

  const [updateAPIToken, mtResponse] = useMutation(
    UPDATE_ACCESS_TOKEN_MUTATION,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
    }
  );

  return {
    canSelectDate: [canSelectDate, setCanSelectDate],
    canSubmit: [canSubmit, setCanSubmit],
    mtResult: [updateAPIToken, mtResponse],
  };
};
