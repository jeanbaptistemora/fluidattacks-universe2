import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck, faMinus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { dateFormatter } from "components/DataTableNext/formatters";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  DEACTIVATE_ORGANIZATION_FINDING_POLICY,
  HANDLE_ORGANIZATION_FINDING_POLICY,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import type { IFindingPoliciesData } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IOrganizationFindingPolicies extends IFindingPoliciesData {
  organizationId: string;
}
const OrganizationFindingPolicy: React.FC<IOrganizationFindingPolicies> = ({
  id,
  lastStatusUpdate,
  name,
  organizationId,
  status,
}: IOrganizationFindingPolicies): JSX.Element => {
  const { t } = useTranslation();
  const { organizationName } = useParams<{ organizationName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDeactivateFindingPolicy: boolean = permissions.can(
    "api_mutations_deactivate_finding_policy_mutate"
  );
  const canHandleFindingPolicy: boolean = permissions.can(
    "api_mutations_handle_finding_policy_acceptation_mutate"
  );
  const [handlePolicyStatus, setHandlePolicyStatus] = useState<
    "APPROVED" | "REJECTED"
  >("APPROVED");

  const [handleOrgFindingPolicy, { loading: handling }] = useMutation(
    HANDLE_ORGANIZATION_FINDING_POLICY,
    {
      onCompleted: (result: {
        handleOrgFindingPolicyAcceptation: { success: boolean };
      }): void => {
        if (result.handleOrgFindingPolicyAcceptation.success) {
          if (handlePolicyStatus === "APPROVED") {
            msgSuccess(
              t(
                "organization.tabs.policies.findings.handlePolicies.success.approved"
              ),
              t("sidebar.newOrganization.modal.successTitle")
            );
          } else {
            msgSuccess(
              t(
                "organization.tabs.policies.findings.handlePolicies.success.rejected"
              ),
              t("sidebar.newOrganization.modal.successTitle")
            );
          }
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Finding name policy not found":
              msgError(
                t("organization.tabs.policies.findings.errors.notFound")
              );
              break;
            case "Exception - This policy has already been reviewed":
              msgError(
                t("organization.tabs.policies.findings.errors.alreadyReviewd")
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.error("Error handling finding policy", message);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId,
          },
        },
      ],
    }
  );

  const [deactivateOrgFindingPolicy, { loading: deactivating }] = useMutation(
    DEACTIVATE_ORGANIZATION_FINDING_POLICY,
    {
      onCompleted: (result: {
        deactivateOrgFindingPolicy: { success: boolean };
      }): void => {
        if (result.deactivateOrgFindingPolicy.success) {
          msgSuccess(
            t("organization.tabs.policies.findings.deactivatePolicies.success"),
            t("sidebar.newOrganization.modal.successTitle")
          );
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (message === "Exception - This policy has already been reviewed") {
            msgError(
              t("organization.tabs.policies.findings.errors.alreadyReviewd")
            );
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("Error deactivating finding policy", message);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId,
          },
        },
      ],
    }
  );

  const isSubmitted: boolean = status === "SUBMITTED";
  const isApproved: boolean = status === "APPROVED";
  const loading: boolean = deactivating || handling;

  async function handleApprovePolicy(): Promise<void> {
    setHandlePolicyStatus("APPROVED");
    await handleOrgFindingPolicy({
      variables: {
        findingPolicyId: id,
        organizationName,
        status: handlePolicyStatus,
      },
    });
  }
  async function handleRejectPolicy(): Promise<void> {
    setHandlePolicyStatus("REJECTED");
    await handleOrgFindingPolicy({
      variables: {
        findingPolicyId: id,
        organizationName,
        status: handlePolicyStatus,
      },
    });
  }
  async function handleDeactivateFindingPolicy(): Promise<void> {
    await deactivateOrgFindingPolicy({
      variables: { findingPolicyId: id, organizationName },
    });
  }

  return (
    <React.StrictMode>
      <div
        className={
          "bt b--light-gray bw1 flex flex-wrap items-center justify-between"
        }
      >
        <div className={"w-50-l w-40-m w-100"}>
          <p className={"f5 ma1 truncate"}>{name}</p>
        </div>
        <div className={"w-20-l w-20-m w-30"}>
          <p className={"f5 ma1 ph1 truncate"}>{status}</p>
        </div>
        <div className={"w-20-l w-20-m w-40"}>
          <p className={"f5 ma1 fr"}>{dateFormatter(lastStatusUpdate)}</p>
        </div>
        {canDeactivateFindingPolicy || canHandleFindingPolicy ? (
          <div className={"w-10-l w-20-m w-30"}>
            {isSubmitted && canHandleFindingPolicy ? (
              <div className={"fr"}>
                <TooltipWrapper
                  displayClass={"dib"}
                  id={"approveButtonToolTip"}
                  message={t(
                    "organization.tabs.policies.findings.tooltip.approveButton"
                  )}
                  placement={"top"}
                >
                  <Button
                    disabled={loading}
                    onClick={handleApprovePolicy}
                    type={"button"}
                  >
                    <FontAwesomeIcon icon={faCheck} />
                  </Button>
                </TooltipWrapper>
                <TooltipWrapper
                  displayClass={"dib"}
                  id={"rejectButtonToolTip"}
                  message={t(
                    "organization.tabs.policies.findings.tooltip.rejectButton"
                  )}
                  placement={"top"}
                >
                  <Button
                    disabled={loading}
                    onClick={handleRejectPolicy}
                    type={"button"}
                  >
                    <FontAwesomeIcon icon={faTimes} />
                  </Button>
                </TooltipWrapper>
              </div>
            ) : undefined}
            {isApproved && canDeactivateFindingPolicy ? (
              <ConfirmDialog
                title={t(
                  "organization.tabs.policies.findings.deactivatePolicies.modalTitle"
                )}
              >
                {(confirm: IConfirmFn): React.ReactNode => {
                  function handleClick(): void {
                    confirm((): void => {
                      void handleDeactivateFindingPolicy();
                    });
                  }

                  return (
                    <div className={"fr"}>
                      <TooltipWrapper
                        displayClass={"dib"}
                        id={"deactivateButtonToolTip"}
                        message={t(
                          "organization.tabs.policies.findings.tooltip.deactivateButton"
                        )}
                        placement={"top"}
                      >
                        <Button
                          disabled={loading}
                          onClick={handleClick}
                          type={"button"}
                        >
                          <FontAwesomeIcon icon={faMinus} />
                        </Button>
                      </TooltipWrapper>
                    </div>
                  );
                }}
              </ConfirmDialog>
            ) : undefined}
          </div>
        ) : undefined}
      </div>
    </React.StrictMode>
  );
};

export { OrganizationFindingPolicy };
