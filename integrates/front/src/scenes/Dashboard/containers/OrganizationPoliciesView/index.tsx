import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button, ButtonOpacity } from "components/Button";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import type {
  IOrganizationPolicies,
  IOrganizationPoliciesData,
  IPoliciesFormData,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/types";
import { VulnerabilityPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/VulnerabilityPolicies/index";
import { ButtonToolbar, Col33L, RowCenter } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import {
  composeValidators,
  isFloatOrInteger,
  isZeroOrPositive,
  numberBetween,
  numeric,
} from "utils/validations";

const tPath = "organization.tabs.policies.";

const OrganizationPolicies: React.FC<IOrganizationPolicies> = (
  props: IOrganizationPolicies
): JSX.Element => {
  const { t } = useTranslation();
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
        msgError(t("groupAlerts.errorTextsad"));
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
      onCompleted: async (): Promise<void> => {
        mixpanel.track("UpdateOrganizationPolicies");
        msgSuccess(t(`${tPath}success`), t(`${tPath}successTitle`));
        await refetchPolicies();
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - Vulnerability grace period value should be a positive integer":
              msgError(t(`${tPath}errors.vulnerabilityGracePeriod`));
              break;
            case "Exception - Acceptance days should be a positive integer":
              msgError(t(`${tPath}errors.maxAcceptanceDays`));
              break;
            case "Exception - Severity value must be a positive floating number between 0.0 and 10.0":
              msgError(t(`${tPath}errors.acceptanceSeverity`));
              break;
            case "Exception - Severity value must be between 0.0 and 10.0":
              msgError(t(`${tPath}errors.invalidBreakableSeverity`));
              break;
            case "Exception - Min acceptance severity value should not be higher than the max value":
              msgError(t(`${tPath}errors.acceptanceSeverityRange`));
              break;
            case "Exception - Number of acceptances should be zero or positive":
              msgError(t(`${tPath}errors.maxNumberAcceptances`));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
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
      header: t(`${tPath}policy`),
      width: "80%",
      wrapped: true,
    },
    {
      dataField: "value",
      header: t(`${tPath}value`),
      width: "20%",
      wrapped: true,
    },
  ];

  const policiesDataSet: Record<string, JSX.Element>[] = [
    {
      name: "maxAcceptanceDays",
      validators: [isZeroOrPositive, numeric],
    },
    {
      name: "maxNumberAcceptances",
      validators: [isZeroOrPositive, numeric],
    },
    {
      fields: ["minAcceptanceSeverity", "maxAcceptanceSeverity"],
      name: "acceptanceSeverityRange",
      validators: [isFloatOrInteger, numberBetween(minSeverity, maxSeverity)],
    },
    {
      name: "vulnerabilityGracePeriod",
      validators: [isZeroOrPositive, numeric],
    },
    {
      name: "minBreakingSeverity",
      validators: [isFloatOrInteger, numberBetween(minSeverity, maxSeverity)],
    },
  ].map(
    ({ name, fields = [], validators }): Record<string, JSX.Element> => ({
      policy: (
        <p>
          {t(`${tPath}policies.${name}`)}
          &nbsp;
          <TooltipWrapper
            displayClass={"di"}
            id={name}
            message={t(`${tPath}recommended.${name}`)}
          >
            <ButtonOpacity disabled={true}>
              <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
            </ButtonOpacity>
          </TooltipWrapper>
        </p>
      ),
      value:
        fields.length > 1 ? (
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
                    name={fields[0]}
                    type={"text"}
                    validate={composeValidators(validators)}
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
                    name={fields[1]}
                    type={"text"}
                    validate={composeValidators(validators)}
                  />
                )}
              </Can>
            </Col33L>
          </RowCenter>
        ) : (
          <Can
            do={"api_mutations_update_organization_policies_mutate"}
            passThrough={true}
          >
            {(canEdit: boolean): JSX.Element => (
              <Field
                component={FormikText}
                disabled={!canEdit}
                name={name}
                type={"text"}
                validate={composeValidators(validators)}
              />
            )}
          </Can>
        ),
    })
  );

  const handleFormSubmit = useCallback(
    async (values: IPoliciesFormData): Promise<void> => {
      await savePolicies({
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
      <p className={"f3 fw7 mt4 mb3"}>{t(`${tPath}title`)}</p>
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
            <Table
              dataset={policiesDataSet}
              exportCsv={false}
              headers={tableHeaders}
              id={"policiesTbl"}
              pageSize={10}
              search={false}
            />
            <Can do={"api_mutations_update_organization_policies_mutate"}>
              {!dirty || loadingPolicies || savingPolicies ? undefined : (
                <ButtonToolbar>
                  <Button
                    disabled={!isValid}
                    onClick={submitForm}
                    variant={"primary"}
                  >
                    {t(`${tPath}save`)}
                  </Button>
                </ButtonToolbar>
              )}
            </Can>
          </Form>
        )}
      </Formik>
      <br />
      <p className={"f3 fw7 mt4 mb3"}>{t(`${tPath}findings.title`)}</p>
      <VulnerabilityPolicies
        organizationId={organizationId}
        vulnerabilityPolicies={_.orderBy(
          data.organization.findingPolicies,
          "lastStatusUpdate",
          "desc"
        )}
      />
    </React.StrictMode>
  );
};

export { OrganizationPolicies };
