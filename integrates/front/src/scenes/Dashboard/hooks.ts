import { ADD_STAKEHOLDER_MUTATION } from "scenes/Dashboard/queries";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import { IAddStakeholderAttr } from "scenes/Dashboard/types";
import { Logger } from "utils/logger";
import { MutationFunction } from "@apollo/react-common";
import React from "react";
import _ from "lodash";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import { msgError, msgSuccess } from "utils/notifications";

export const useAddStakeholder: () => readonly [
  MutationFunction,
  boolean,
  React.Dispatch<React.SetStateAction<boolean>>
] = (): readonly [
  MutationFunction,
  boolean,
  React.Dispatch<React.SetStateAction<boolean>>
] => {
  const { t } = useTranslation();

  // Handle modal state
  const [isOpen, toggle] = React.useState(false);

  // Handle mutation results
  const handleOnSuccess: (mtResult: IAddStakeholderAttr) => void = (
    mtResult: IAddStakeholderAttr
  ): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.addStakeholder.success) {
        toggle(false);
        msgSuccess(
          t("userModal.success", {
            email: mtResult.addStakeholder.email,
          }),
          t("search_findings.tab_users.title_success")
        );
      }
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred adding user", error);
      msgError(t("group_alerts.error_textsad"));
    });
  };

  const [addStakeholder] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: handleOnSuccess,
    onError: handleOnError,
  });

  return [addStakeholder, isOpen, toggle] as const;
};
