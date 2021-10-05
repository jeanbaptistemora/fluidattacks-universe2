import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faArrowRight,
  faCheck,
  faMinus,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import styled from "styled-components";

import {
  handleOrgFindingPolicyDeactivation,
  handleOrgFindingPolicyDeactivationError,
  handleOrgFindingPolicyError,
  handleOrgFindingPolicyNotification,
  handleSubmitOrganizationFindingPolicy,
  handleSubmitOrganizationFindingPolicyError,
} from "./helpers";

import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper";
import { statusFormatter } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/formatter";
import {
  DEACTIVATE_ORGANIZATION_FINDING_POLICY,
  HANDLE_ORGANIZATION_FINDING_POLICY,
  RESUBMIT_ORGANIZATION_FINDING_POLICY,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import type { IFindingPoliciesData } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { formatIsoDate } from "utils/date";

const StyledText = styled.input.attrs({
  className: "w-100 pa2 lh-copy bg-white bw0",
})``;

interface IOrganizationFindingPolicies extends IFindingPoliciesData {
  organizationId: string;
}
const OrganizationFindingPolicy: React.FC<IOrganizationFindingPolicies> = ({
  id,
  lastStatusUpdate,
  name,
  organizationId,
  status,
  tags,
}: IOrganizationFindingPolicies): JSX.Element => {
  const { t } = useTranslation();
  const { organizationName } = useParams<{ organizationName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDeactivateFindingPolicy: boolean = permissions.can(
    "api_mutations_deactivate_organization_finding_policy_mutate"
  );
  const canHandleFindingPolicy: boolean = permissions.can(
    "api_mutations_handle_organization_finding_policy_acceptation_mutate"
  );
  const canResubmitFindingPolicy: boolean = permissions.can(
    "api_mutations_submit_organization_finding_policy_mutate"
  );
  const [handlePolicyStatus, setHandlePolicyStatus] =
    useState<"APPROVED" | "REJECTED">("APPROVED");

  const [handleOrgFindingPolicy, { loading: handling }] = useMutation(
    HANDLE_ORGANIZATION_FINDING_POLICY,
    {
      onCompleted: (result: {
        handleOrganizationFindingPolicyAcceptance: { success: boolean };
      }): void => {
        handleOrgFindingPolicyNotification(
          result,
          handlePolicyStatus,
          organizationName
        );
      },
      onError: (error: ApolloError): void => {
        handleOrgFindingPolicyError(error);
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

  const [deactivateOrganizationFindingPolicy, { loading: deactivating }] =
    useMutation(DEACTIVATE_ORGANIZATION_FINDING_POLICY, {
      onCompleted: (result: {
        deactivateOrganizationFindingPolicy: { success: boolean };
      }): void => {
        handleOrgFindingPolicyDeactivation(result, organizationName);
      },
      onError: (error: ApolloError): void => {
        handleOrgFindingPolicyDeactivationError(error);
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId,
          },
        },
      ],
    });

  const [resubmitOrganizationFindingPolicy, { loading: submitting }] =
    useMutation(RESUBMIT_ORGANIZATION_FINDING_POLICY, {
      onCompleted: (result: {
        submitOrganizationFindingPolicy: { success: boolean };
      }): void => {
        handleSubmitOrganizationFindingPolicy(result, organizationName);
      },
      onError: (error: ApolloError): void => {
        handleSubmitOrganizationFindingPolicyError(error);
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId,
          },
        },
      ],
    });

  const isResubmitable: boolean =
    status === "INACTIVE" || status === "REJECTED";
  const isSubmitted: boolean = status === "SUBMITTED";
  const isApproved: boolean = status === "APPROVED";
  const loading: boolean = deactivating || handling;

  async function handleApprovePolicy(): Promise<void> {
    setHandlePolicyStatus("APPROVED");
    await handleOrgFindingPolicy({
      variables: {
        findingPolicyId: id,
        organizationName,
        status: "APPROVED",
      },
    });
  }
  async function handleRejectPolicy(): Promise<void> {
    setHandlePolicyStatus("REJECTED");
    await handleOrgFindingPolicy({
      variables: {
        findingPolicyId: id,
        organizationName,
        status: "REJECTED",
      },
    });
  }
  async function handleDeactivateFindingPolicy(): Promise<void> {
    await deactivateOrganizationFindingPolicy({
      variables: { findingPolicyId: id, organizationName },
    });
  }
  async function handleResubmitFindingPolicy(): Promise<void> {
    await resubmitOrganizationFindingPolicy({
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
        <div className={"w-40-l w-100-m w-100"}>
          <p className={"f5 ma1 truncate"}>{name}</p>
        </div>
        <div className={"w-20-l w-30-m w-100"}>
          <StyledText
            disabled={true}
            id={"tags"}
            name={"tags"}
            type={"text"}
            value={tags.join(", ")}
          />
        </div>
        <div className={"w-10-l w-30-m w-30"}>
          <p className={"f5 ml1 mr1 mt2 mb2 ph1 truncate"}>
            {statusFormatter(status)}
          </p>
        </div>
        <div className={"w-20-l w-20-m w-40"}>
          <p className={"f5 ma1 fr"}>{formatIsoDate(lastStatusUpdate)}</p>
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
            {isResubmitable && canResubmitFindingPolicy ? (
              <ConfirmDialog
                title={t(
                  "organization.tabs.policies.findings.submitPolicies.modalTitle"
                )}
              >
                {(confirm: IConfirmFn): React.ReactNode => {
                  function handleClick(): void {
                    confirm((): void => {
                      void handleResubmitFindingPolicy();
                    });
                  }

                  return (
                    <div className={"fr"}>
                      <TooltipWrapper
                        displayClass={"dib"}
                        id={"resubmitButtonToolTip"}
                        message={t(
                          "organization.tabs.policies.findings.tooltip.resubmitButton"
                        )}
                        placement={"top"}
                      >
                        <Button
                          disabled={submitting}
                          onClick={handleClick}
                          type={"button"}
                        >
                          <FontAwesomeIcon icon={faArrowRight} />
                        </Button>
                      </TooltipWrapper>
                    </div>
                  );
                }}
              </ConfirmDialog>
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
