import type { ApolloError } from "@apollo/client";
import { useLazyQuery, useQuery } from "@apollo/client";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  GET_GROUP_UNFULFILLED_STANDARDS,
  GET_UNFULFILLED_STANDARD_REPORT_URL,
} from "./queries";
import type {
  IGroupAttr,
  IOrganizationComplianceStandardsProps,
  IUnfulfilledStandardAttr,
} from "./types";
import { UnfulfilledStandardCard } from "./UnfulfilledStandardCard";

import { Button } from "components/Button";
import { Select } from "components/Input";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { GET_ORGANIZATION_GROUP_NAMES } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

const OrganizationComplianceStandardsView: React.FC<IOrganizationComplianceStandardsProps> =
  (props: IOrganizationComplianceStandardsProps): JSX.Element => {
    const { organizationId } = props;
    const { t } = useTranslation();

    // Handle state
    const [selectedGroupName, setSelectedGroupName] = useState<
      string | undefined
    >(undefined);
    const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);
    const [disableVerify, setDisableVerify] = useState(false);

    // GraphQL queries
    const { data: groupsData } = useQuery<{
      organization: { groups: IGroupAttr[] };
    }>(GET_ORGANIZATION_GROUP_NAMES, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading organization group names",
            error
          );
        });
      },
      variables: {
        organizationId,
      },
    });
    const { data: unfulfilledStandardsData } = useQuery<{
      group: {
        compliance: { unfulfilledStandards: IUnfulfilledStandardAttr[] };
      };
    }>(GET_GROUP_UNFULFILLED_STANDARDS, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading group unfulfilled standards",
            error
          );
        });
      },
      skip: _.isUndefined(selectedGroupName) || _.isEmpty(selectedGroupName),
      variables: {
        groupName: selectedGroupName,
      },
    });
    const [requestUnfulfilledStandardReport] = useLazyQuery<{
      unfulfilledStandardReportUrl: string;
    }>(GET_UNFULFILLED_STANDARD_REPORT_URL, {
      onCompleted: (data): void => {
        setDisableVerify(false);
        openUrl(data.unfulfilledStandardReportUrl);
        msgSuccess(
          t(
            "organization.tabs.compliance.tabs.standards.alerts.generatedReport"
          ),
          t("groupAlerts.titleSuccess")
        );
        setIsVerifyDialogOpen(false);
      },
      onError: (errors: ApolloError): void => {
        setDisableVerify(false);
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Stakeholder could not be verified":
              msgError(
                t("group.findings.report.alerts.nonVerifiedStakeholder")
              );
              break;
            case "Exception - The verification code is invalid":
              msgError(
                t("group.findings.report.alerts.invalidVerificationCode")
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred requesting group report",
                error
              );
          }
        });
      },
    });

    // Format data
    const groups = useMemo(
      (): IGroupAttr[] =>
        _.isUndefined(groupsData) ? [] : groupsData.organization.groups,
      [groupsData]
    );
    const unfulfilledStandards = _.isUndefined(unfulfilledStandardsData)
      ? []
      : unfulfilledStandardsData.group.compliance.unfulfilledStandards;

    // Handle effects
    useEffect((): void => {
      if (_.isUndefined(selectedGroupName) && groups.length > 0) {
        setSelectedGroupName(groups[0].name);
      }
    }, [groups, selectedGroupName]);

    // Handle actions
    const onGroupChange = useCallback(
      (event: React.ChangeEvent<HTMLSelectElement>): void => {
        event.preventDefault();
        setSelectedGroupName(event.target.value);
      },
      []
    );
    function onSubmit(): void {
      // OnSubmit
    }
    function handleRequestUnfulfilledStandardReport(
      verificationCode: string
    ): void {
      setDisableVerify(true);
      requestUnfulfilledStandardReport({
        variables: {
          groupName: selectedGroupName,
          verificationCode,
        },
      });
      mixpanel.track("UnfulfilledStandardReportRequest");
    }

    return (
      <React.StrictMode>
        <Row>
          <Col lg={50} md={50} sm={50}>
            <Formik
              initialValues={{
                groupName: selectedGroupName,
              }}
              name={"selectGroup"}
              onSubmit={onSubmit}
            >
              <div className={"flex flex-row  justify-start items-end "}>
                <div>
                  <Text disp={"inline"} fw={7} mb={3} mt={2} size={"big"}>
                    {t(
                      "organization.tabs.compliance.tabs.standards.unfulfilledStandards.title"
                    )}
                    {_.isUndefined(unfulfilledStandardsData)
                      ? undefined
                      : ` (${unfulfilledStandards.length})`}
                  </Text>
                </div>
                &emsp;
                <div>
                  <Select name={"groupName"} onChange={onGroupChange}>
                    {groups.map(
                      (group: IGroupAttr): JSX.Element => (
                        <option key={group.name} value={group.name}>
                          {_.startCase(group.name)}
                        </option>
                      )
                    )}
                  </Select>
                </div>
              </div>
            </Formik>
          </Col>
          <Col lg={50} md={50} sm={50}>
            <div className={"flex flex-row  justify-end items-end "}>
              <VerifyDialog disable={disableVerify} isOpen={isVerifyDialogOpen}>
                {(setVerifyCallbacks): JSX.Element => {
                  function onRequestReport(): void {
                    setVerifyCallbacks(
                      (verificationCode: string): void => {
                        handleRequestUnfulfilledStandardReport(
                          verificationCode
                        );
                      },
                      (): void => {
                        setIsVerifyDialogOpen(false);
                      }
                    );
                    setIsVerifyDialogOpen(true);
                  }

                  return (
                    <Tooltip
                      id={
                        "organization.tabs.compliance.tabs.standards.buttons.generateReport.tooltip"
                      }
                      tip={t(
                        "organization.tabs.compliance.tabs.standards.buttons.generateReport.tooltip"
                      )}
                    >
                      <Button
                        id={"unfulfilled-standard-report-pdf"}
                        onClick={onRequestReport}
                        variant={"primary"}
                      >
                        {t(
                          "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
                        )}
                        &nbsp;
                        <FontAwesomeIcon
                          fontSize={17}
                          fontWeight={40}
                          icon={faArrowRight}
                        />
                      </Button>
                    </Tooltip>
                  );
                }}
              </VerifyDialog>
            </div>
          </Col>
        </Row>
        <br />
        <Row>
          <Col lg={100} md={100} sm={100}>
            <Row>
              {_.sortBy(
                unfulfilledStandards,
                (unfulfilledStandard: IUnfulfilledStandardAttr): string =>
                  unfulfilledStandard.title.toUpperCase()
              ).map(
                (
                  unfulfilledStandard: IUnfulfilledStandardAttr
                ): JSX.Element => (
                  <Col key={unfulfilledStandard.title} lg={25} md={50} sm={100}>
                    <UnfulfilledStandardCard
                      unfulfilledStandard={unfulfilledStandard}
                    />
                  </Col>
                )
              )}
            </Row>
          </Col>
        </Row>
      </React.StrictMode>
    );
  };

export { OrganizationComplianceStandardsView };
