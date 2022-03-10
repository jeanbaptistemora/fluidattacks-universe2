import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import { track } from "mixpanel-browser";

import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleOrgFindingPolicyNotification = (
  result: {
    handleOrganizationFindingPolicyAcceptance: { success: boolean };
  },
  handlePolicyStatus: "APPROVED" | "REJECTED",
  organizationName: string
): void => {
  if (result.handleOrganizationFindingPolicyAcceptance.success) {
    if (handlePolicyStatus === "APPROVED") {
      track("ApproveOrganizationFindingPolicy", {
        Organization: organizationName,
      });
      msgSuccess(
        translate.t(
          "organization.tabs.policies.findings.handlePolicies.success.approved"
        ),
        translate.t("sidebar.newOrganization.modal.successTitle")
      );
    } else {
      track("RejectOrganizationFindingPolicy", {
        Organization: organizationName,
      });
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

const handleOrgFindingPolicyDeactivation = (
  result: {
    deactivateOrganizationFindingPolicy: { success: boolean };
  },
  organizationName: string
): void => {
  if (result.deactivateOrganizationFindingPolicy.success) {
    track("DeactivateOrganizationFindingPolicy", {
      Organization: organizationName,
    });
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

const handleSubmitOrganizationFindingPolicy = (
  result: {
    submitOrganizationFindingPolicy: { success: boolean };
  },
  organizationName: string
): void => {
  if (result.submitOrganizationFindingPolicy.success) {
    track("ReSubmitOrganizationFindingPolicy", {
      Organization: organizationName,
    });
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
