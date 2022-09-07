/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type {
  ApolloError,
  ApolloQueryResult,
  OperationVariables,
} from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";

import type { IHeaderQueryResult } from "./types";

import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleSuccessfulDraft = (
  result: {
    submitDraft: { success: boolean };
  },
  headerRefetch: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IHeaderQueryResult>>
): void => {
  if (result.submitDraft.success) {
    msgSuccess(
      translate.t("group.drafts.successSubmit"),
      translate.t("group.drafts.titleSuccess")
    );
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void headerRefetch(); //NOSONAR
  }
};

const handleDraftError = (
  submitError: ApolloError,
  headerRefetch: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IHeaderQueryResult>>
): void => {
  submitError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    if (_.includes(message, "Exception - This draft has missing fields")) {
      msgError(
        translate.t("group.drafts.errorSubmit", {
          missingFields: message.split("fields: ")[1],
        })
      );
    } else if (
      message === "Exception - This draft has already been submitted"
    ) {
      msgError(translate.t("groupAlerts.draftAlreadySubmitted"));
      // Exception: FP(void operator is necessary)
      // eslint-disable-next-line
        void headerRefetch(); //NOSONAR
    } else if (message === "Exception - This draft has already been approved") {
      msgError(translate.t("groupAlerts.draftAlreadyApproved"));
      // Exception: FP(void operator is necessary)
      // eslint-disable-next-line
        void headerRefetch(); //NOSONAR
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred submitting draft", submitError);
    }
  });
};

const handleDraftApproval = (
  result: { approveDraft: { success: boolean } },
  headerRefetch: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IHeaderQueryResult>>
): void => {
  if (result.approveDraft.success) {
    msgSuccess(
      translate.t("searchFindings.draftApproved"),
      translate.t("group.drafts.titleSuccess")
    );
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void headerRefetch(); //NOSONAR
  }
};

const handleDraftApprovalError = (
  approveError: ApolloError,
  headerRefetch: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IHeaderQueryResult>>
): void => {
  approveError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - This draft has already been approved":
        msgError(translate.t("groupAlerts.draftAlreadyApproved"));
        // Exception: FP(void operator is necessary)
        // eslint-disable-next-line
          void headerRefetch(); //NOSONAR
        break;
      case "Exception - The draft has not been submitted yet":
        msgError(translate.t("groupAlerts.draftNotSubmitted"));
        // Exception: FP(void operator is necessary)
        // eslint-disable-next-line
          void headerRefetch(); //NOSONAR
        break;
      case "CANT_APPROVE_FINDING_WITHOUT_VULNS":
        msgError(translate.t("groupAlerts.draftWithoutVulns"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred approving draft", approveError);
    }
  });
};

export {
  handleSuccessfulDraft,
  handleDraftError,
  handleDraftApproval,
  handleDraftApprovalError,
};
