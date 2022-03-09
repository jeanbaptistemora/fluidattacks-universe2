import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import { FindingPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/index";
import style from "scenes/Dashboard/containers/OrganizationPoliciesView/index.css";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import type {
  IOrganizationPolicies,
  IOrganizationPoliciesData,
  IPoliciesFormData,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/types";
import { ButtonToolbar, Col33L, RowCenter } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  isFloatOrInteger,
  isZeroOrPositive,
  numberBetween,
  numeric,
} from "utils/validations";

const OrganizationPolicies: React.FC<IOrganizationPolicies> = (
  props: IOrganizationPolicies
): JSX.Element => {
  // State management
  const minSeverity: number = 0.0;
  const maxSeverity: number = 10.0;
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();

  // GraphQL Operations
  const {
    data,
    loading: loadingPolicies,
    refetch: refetchPolicies,
  } = useQuery<IOrganizationPoliciesData>(GET_ORGANIZATION_POLICIES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred fetching organization policies",
          error
        );
      });
    },
    variables: { organizationId },
  });

  const [savePolicies, { loading: savingPolicies }] = useMutation(
    UPDATE_ORGANIZATION_POLICIES,
    {
      onCompleted: (): void => {
        track("UpdateOrganizationPolicies");
        msgSuccess(
          translate.t("organization.tabs.policies.success"),
          translate.t("organization.tabs.policies.successTitle")
        );

        void refetchPolicies();
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Vulnerability grace period value should be a positive integer":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.vulnerabilityGracePeriod"
                )
              );
              break;
            case "Exception - Acceptance days should be a positive integer":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.maxAcceptanceDays"
                )
              );
              break;
            case "Exception - Severity value must be a positive floating number between 0.0 and 10.0":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.acceptanceSeverity"
                )
              );
              break;
            case "Exception - Severity value must be between 0.0 and 10.0":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.invalidBreakableSeverity"
                )
              );
              break;
            case "Exception - Min acceptance severity value should not be higher than the max value":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.acceptanceSeverityRange"
                )
              );
              break;
            case "Exception - Number of acceptances should be zero or positive":
              msgError(
                translate.t(
                  "organization.tabs.policies.errors.maxNumberAcceptances"
                )
              );
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating the organization policies",
                error
              );
          }
        });
      },
    }
  );

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "policy",
      header: translate.t("organization.tabs.policies.policy"),
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "value",
      header: translate.t("organization.tabs.policies.value"),
      width: "25%",
      wrapped: true,
    },
    {
      dataField: "recommended",
      header: translate.t("organization.tabs.policies.recommended.title"),
      width: "25%",
      wrapped: true,
    },
  ];

  const policiesDataSet: Record<string, JSX.Element>[] = [
    {
      policy: (
        <p>
          {translate.t("organization.tabs.policies.policies.maxAcceptanceDays")}
        </p>
      ),
      recommended: (
        <p className={style.recommended}>
          {translate.t("organization.tabs.policies.recommended.acceptanceDays")}
        </p>
      ),
      value: (
        <Can
          do={"api_mutations_update_organization_policies_mutate"}
          passThrough={true}
        >
          {(canEdit: boolean): JSX.Element => (
            <Field
              component={FormikText}
              disabled={!canEdit}
              name={"maxAcceptanceDays"}
              type={"text"}
              validate={composeValidators([isZeroOrPositive, numeric])}
            />
          )}
        </Can>
      ),
    },
    {
      policy: (
        <p>
          {translate.t(
            "organization.tabs.policies.policies.maxNumberAcceptances"
          )}
        </p>
      ),
      recommended: (
        <p className={style.recommended}>
          {translate.t(
            "organization.tabs.policies.recommended.numberAcceptances"
          )}
        </p>
      ),
      value: (
        <Can
          do={"api_mutations_update_organization_policies_mutate"}
          passThrough={true}
        >
          {(canEdit: boolean): JSX.Element => (
            <Field
              component={FormikText}
              disabled={!canEdit}
              name={"maxNumberAcceptances"}
              type={"text"}
              validate={composeValidators([isZeroOrPositive, numeric])}
            />
          )}
        </Can>
      ),
    },
    {
      policy: (
        <p>
          {translate.t(
            "organization.tabs.policies.policies.vulnerabilityGracePeriod"
          )}
        </p>
      ),
      recommended: (
        <p className={style.recommended}>
          {translate.t(
            "organization.tabs.policies.recommended.vulnerabilityGracePeriod"
          )}
        </p>
      ),
      value: (
        <Can
          do={"api_mutations_update_organization_policies_mutate"}
          passThrough={true}
        >
          {(canEdit: boolean): JSX.Element => (
            <Field
              component={FormikText}
              disabled={!canEdit}
              name={"vulnerabilityGracePeriod"}
              type={"text"}
              validate={composeValidators([isZeroOrPositive, numeric])}
            />
          )}
        </Can>
      ),
    },
    {
      policy: (
        <p>
          {translate.t(
            "organization.tabs.policies.policies.minBreakingSeverity"
          )}
        </p>
      ),
      recommended: (
        <p className={style.recommended}>
          {translate.t(
            "organization.tabs.policies.recommended.breakableSeverity"
          )}
        </p>
      ),
      value: (
        <Can
          do={"api_mutations_update_organization_policies_mutate"}
          passThrough={true}
        >
          {(canEdit: boolean): JSX.Element => (
            <Field
              component={FormikText}
              disabled={!canEdit}
              name={"minBreakingSeverity"}
              type={"text"}
              validate={composeValidators([
                isFloatOrInteger,
                numberBetween(minSeverity, maxSeverity),
              ])}
            />
          )}
        </Can>
      ),
    },
    {
      policy: (
        <p>
          {translate.t(
            "organization.tabs.policies.policies.acceptanceSeverityRange"
          )}
        </p>
      ),
      recommended: (
        <p className={style.recommended}>
          {translate.t(
            "organization.tabs.policies.recommended.acceptanceSeverity"
          )}
        </p>
      ),
      value: (
        <div>
          <RowCenter>
            <Col33L>
              <Can
                do={"api_mutations_update_organization_policies_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Field
                    component={FormikText}
                    disabled={!canEdit}
                    name={"minAcceptanceSeverity"}
                    type={"text"}
                    validate={composeValidators([
                      isFloatOrInteger,
                      numberBetween(minSeverity, maxSeverity),
                    ])}
                  />
                )}
              </Can>
            </Col33L>
            {/* eslint-disable-next-line react/forbid-component-props */}
            <Col33L className={"tc"}>
              <p>{"-"}</p>
            </Col33L>
            <Col33L>
              <Can
                do={"api_mutations_update_organization_policies_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Field
                    component={FormikText}
                    disabled={!canEdit}
                    name={"maxAcceptanceSeverity"}
                    type={"text"}
                    validate={composeValidators([
                      isFloatOrInteger,
                      numberBetween(minSeverity, maxSeverity),
                    ])}
                  />
                )}
              </Can>
            </Col33L>
          </RowCenter>
        </div>
      ),
    },
  ];

  const handleFormSubmit = useCallback(
    (values: IPoliciesFormData): void => {
      void savePolicies({
        variables: {
          maxAcceptanceDays: parseInt(values.maxAcceptanceDays, 10),
          maxAcceptanceSeverity: parseFloat(values.maxAcceptanceSeverity),
          maxNumberAcceptances: parseInt(values.maxNumberAcceptances, 10),
          minAcceptanceSeverity: parseFloat(values.minAcceptanceSeverity),
          minBreakingSeverity: parseFloat(values.minBreakingSeverity),
          organizationId,
          organizationName: organizationName.toLowerCase(),
          vulnerabilityGracePeriod: parseInt(
            values.vulnerabilityGracePeriod,
            10
          ),
        },
      });
    },
    [organizationId, organizationName, savePolicies]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          maxAcceptanceDays: _.isNull(data.organization.maxAcceptanceDays)
            ? ""
            : data.organization.maxAcceptanceDays.toString(),
          maxAcceptanceSeverity: parseFloat(
            data.organization.maxAcceptanceSeverity
          )
            .toFixed(1)
            .toString(),
          maxNumberAcceptances: _.isNull(data.organization.maxNumberAcceptances)
            ? ""
            : data.organization.maxNumberAcceptances.toString(),
          minAcceptanceSeverity: parseFloat(
            data.organization.minAcceptanceSeverity
          )
            .toFixed(1)
            .toString(),
          minBreakingSeverity: _.isNull(data.organization.minBreakingSeverity)
            ? "0.0"
            : parseFloat(data.organization.minBreakingSeverity)
                .toFixed(1)
                .toString(),
          vulnerabilityGracePeriod: _.isNull(
            data.organization.vulnerabilityGracePeriod
          )
            ? ""
            : data.organization.vulnerabilityGracePeriod.toString(),
        }}
        name={"orgPolicies"}
        onSubmit={handleFormSubmit}
      >
        {({ dirty, isValid, submitForm }): JSX.Element => (
          <Form id={"orgPolicies"}>
            <TooltipWrapper
              id={translate.t(
                "organization.tabs.policies.permissionTooltip.id"
              )}
              message={translate.t(
                "organization.tabs.policies.permissionTooltip"
              )}
            >
              <Table
                bordered={true}
                dataset={policiesDataSet}
                exportCsv={false}
                headers={tableHeaders}
                id={"policiesTbl"}
                pageSize={10}
                search={false}
                striped={true}
              />
            </TooltipWrapper>
            <Can do={"api_mutations_update_organization_policies_mutate"}>
              {!dirty || loadingPolicies || savingPolicies ? undefined : (
                <ButtonToolbar>
                  <Button
                    disabled={!isValid}
                    onClick={submitForm}
                    variant={"primary"}
                  >
                    {translate.t("organization.tabs.policies.save")}
                  </Button>
                </ButtonToolbar>
              )}
            </Can>
          </Form>
        )}
      </Formik>
      <br />
      <p className={"mb0 f4 tc"}>
        <b>{translate.t("organization.tabs.policies.findings.title")}</b>
      </p>
      <hr className={"b--light-gray bw2 mt0"} />
      <FindingPolicies
        findingPolicies={_.orderBy(
          data.organization.findingPolicies,
          "lastStatusUpdate",
          "desc"
        )}
        organizationId={organizationId}
      />
    </React.StrictMode>
  );
};

export { OrganizationPolicies };
