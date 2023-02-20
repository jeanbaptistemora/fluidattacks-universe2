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

const handleSuccessfulDraft = async (
  result: {
    submitDraft: { success: boolean };
  },
  headerRefetch: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IHeaderQueryResult>>
): Promise<void> => {
  if (result.submitDraft.success) {
    msgSuccess(
      translate.t("group.drafts.successSubmit"),
      translate.t("group.drafts.titleSuccess")
    );
    await headerRefetch();
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
  approveError.graphQLErrors.forEach(
    async ({ message }: GraphQLError): Promise<void> => {
      if (_.includes(message, "Exception - This draft has missing fields")) {
        msgError(
          translate.t("groupAlerts.errorApprove", {
            missingFields: message.split("fields: ")[1],
          })
        );

        return;
      }

      switch (message) {
        case "Exception - This draft has already been approved":
          msgError(translate.t("groupAlerts.draftAlreadyApproved"));
          await headerRefetch();
          break;
        case "Exception - The draft has not been submitted yet":
          msgError(translate.t("groupAlerts.draftNotSubmitted"));
          await headerRefetch();
          break;
        case "CANT_APPROVE_FINDING_WITHOUT_VULNS":
          msgError(translate.t("groupAlerts.draftWithoutVulns"));
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred approving draft", approveError);
      }
    }
  );
};

export {
  handleSuccessfulDraft,
  handleDraftError,
  handleDraftApproval,
  handleDraftApprovalError,
};
