import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleOrgFindingPolicyNotification = (
  result: {
    handleOrgFindingPolicyAcceptation: { success: boolean };
  },
  handlePolicyStatus: "APPROVED" | "REJECTED"
): void => {
  if (result.handleOrgFindingPolicyAcceptation.success) {
    if (handlePolicyStatus === "APPROVED") {
      msgSuccess(
        translate.t(
          "organization.tabs.policies.findings.handlePolicies.success.approved"
        ),
        translate.t("sidebar.newOrganization.modal.successTitle")
      );
    } else {
      msgSuccess(
        translate.t(
          "organization.tabs.policies.findings.handlePolicies.success.rejected"
        ),
        translate.t("sidebar.newOrganization.modal.successTitle")
      );
    }
  }
};

const handleOrgFindingPolicyError = (error: ApolloError): void => {
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Finding name policy not found":
        msgError(
          translate.t("organization.tabs.policies.findings.errors.notFound")
        );
        break;
      case "Exception - This policy has already been reviewed":
        msgError(
          translate.t(
            "organization.tabs.policies.findings.errors.alreadyReviewd"
          )
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("Error handling finding policy", message);
    }
  });
};

const handleOrgFindingPolicyDeactivation = (result: {
  deactivateOrgFindingPolicy: { success: boolean };
}): void => {
  if (result.deactivateOrgFindingPolicy.success) {
    msgSuccess(
      translate.t(
        "organization.tabs.policies.findings.deactivatePolicies.success"
      ),
      translate.t("sidebar.newOrganization.modal.successTitle")
    );
  }
};

const handleOrgFindingPolicyDeactivationError = (error: ApolloError): void => {
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    if (message === "Exception - This policy has already been reviewed") {
      msgError(
        translate.t("organization.tabs.policies.findings.errors.alreadyReviewd")
      );
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("Error deactivating finding policy", message);
    }
  });
};

const handleSubmitOrganizationFindingPolicy = (result: {
  submitOrganizationFindingPolicy: { success: boolean };
}): void => {
  if (result.submitOrganizationFindingPolicy.success) {
    msgSuccess(
      translate.t("organization.tabs.policies.findings.addPolicies.success"),
      translate.t("sidebar.newOrganization.modal.successTitle")
    );
  }
};

const handleSubmitOrganizationFindingPolicyError = (
  error: ApolloError
): void => {
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    if (message === "Exception - This policy has already been reviewed") {
      msgError(
        translate.t("organization.tabs.policies.findings.errors.alreadyReviewd")
      );
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("Error re-submitting finding policy", message);
    }
  });
};

export {
  handleOrgFindingPolicyNotification,
  handleOrgFindingPolicyError,
  handleOrgFindingPolicyDeactivation,
  handleOrgFindingPolicyDeactivationError,
  handleSubmitOrganizationFindingPolicy,
  handleSubmitOrganizationFindingPolicyError,
};
