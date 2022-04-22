import type { ApolloError, MutationFunction } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type React from "react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { ADD_STAKEHOLDER_MUTATION } from "scenes/Dashboard/queries";
import type { IAddStakeholderAttr } from "scenes/Dashboard/types";
import { Logger } from "utils/logger";
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
  const [isOpen, setIsOpen] = useState(false);

  // Handle mutation results
  const handleOnSuccess: (mtResult: IAddStakeholderAttr) => void = (
    mtResult: IAddStakeholderAttr
  ): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.addStakeholder.success) {
        setIsOpen(false);
        msgSuccess(
          t("userModal.success", {
            email: mtResult.addStakeholder.email,
          }),
          t("searchFindings.tabUsers.titleSuccess")
        );
      }
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred adding user", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const [addStakeholder] = useMutation(ADD_STAKEHOLDER_MUTATION, {
    onCompleted: handleOnSuccess,
    onError: handleOnError,
  });

  return [addStakeholder, isOpen, setIsOpen] as const;
};
