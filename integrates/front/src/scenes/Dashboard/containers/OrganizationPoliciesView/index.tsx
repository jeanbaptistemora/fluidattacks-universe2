import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useSelector } from "react-redux";
import { useParams } from "react-router";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { IHeaderConfig } from "components/DataTableNext/types";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { default as style } from "scenes/Dashboard/containers/OrganizationPoliciesView/index.css";
import {
  GET_ORGANIZATION_POLICIES,
  UPDATE_ORGANIZATION_POLICIES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { IOrganizationPolicies, IPoliciesFormData } from "scenes/Dashboard/containers/OrganizationPoliciesView/types";
import { ButtonToolbar, Col33L, RowCenter } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const organizationPolicies: React.FC<IOrganizationPolicies> = (props: IOrganizationPolicies): JSX.Element => {

  // State management
  const { organizationId } = props;
  const { organizationName } = useParams<{ organizationName: string }>();
  const selector: (state: {}, ...fields: string[]) => IPoliciesFormData = formValueSelector("orgPolicies");
  const formValues: IPoliciesFormData = useSelector((state: {}) =>
    selector(state, "maxAcceptanceDays", "maxAcceptanceSeverity", "maxNumberAcceptations", "minAcceptanceSeverity"));

  // GraphQL Operations
  const {
    data,
    loading: loadingPolicies,
    refetch: refetchPolicies,
  } = useQuery(GET_ORGANIZATION_POLICIES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning(
          "An error occurred fetching organization policies",
          error,
        );
      });
    },
    variables: { organizationId },
  });

  const [savePolicies, { loading: savingPolicies }] = useMutation(UPDATE_ORGANIZATION_POLICIES, {
    onCompleted: (): void => {
      mixpanel.track("UpdateOrganizationPolicies", formValues);
      msgSuccess(
        translate.t("organization.tabs.policies.success"),
        translate.t("organization.tabs.policies.success_title"),
      );

      refetchPolicies();
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        let msg: string;

        switch (message) {
          case "Exception - Acceptance days should be a positive integer":
            msg = "organization.tabs.policies.errors.maxAcceptanceDays";
            break;
          case "Exception - Severity value should be a positive floating number between 0.0 a 10.0":
            msg = "organization.tabs.policies.errors.acceptanceSeverity";
            break;
          case "Exception - Min acceptance severity value should not be higher than the max value":
            msg = "organization.tabs.policies.errors.acceptanceSeverityRange";
            break;
          case "Exception - Number of acceptations should be zero or positive":
            msg = "organization.tabs.policies.errors.maxNumberAcceptations";
            break;
          default:
            msg = "group_alerts.error_textsad";
            Logger.warning("An error occurred updating the organization policies", error);
        }
        msgError(translate.t(msg));
      });
    },
    variables: {
      maxAcceptanceDays: parseInt(formValues.maxAcceptanceDays, 10),
      maxAcceptanceSeverity: parseFloat(formValues.maxAcceptanceSeverity),
      maxNumberAcceptations: parseInt(formValues.maxNumberAcceptations, 10),
      minAcceptanceSeverity: parseFloat(formValues.minAcceptanceSeverity),
      organizationId,
      organizationName: organizationName.toLowerCase(),
    },
  });

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

  const policiesDataSet: Array<Record<string, JSX.Element>> = [
    {
      policy: (
      <p>{translate.t("organization.tabs.policies.policies.maxAcceptanceDays")}</p>
      ),
      recommended: (
      <p className={style.recommended}>{translate.t("organization.tabs.policies.recommended.acceptanceDays")}</p>
      ),
      value: (
        <Field
          component={Text}
          name="maxAcceptanceDays"
          type="text"
        />
      ),
    },
    {
      policy: (
      <p>{translate.t("organization.tabs.policies.policies.acceptanceSeverityRange")}</p>
      ),
      recommended: (
      <p className={style.recommended}>{translate.t("organization.tabs.policies.recommended.acceptanceSeverity")}</p>
      ),
      value: (
        <React.Fragment>
          <div>
            <RowCenter>
              <Col33L>
                <Field
                  component={Text}
                  name="minAcceptanceSeverity"
                  type="text"
                />
              </Col33L>
              <Col33L className={"tc"}>
                <p>-</p>
              </Col33L>
              <Col33L>
                <Field
                  component={Text}
                  name="maxAcceptanceSeverity"
                  type="text"
                />
              </Col33L>
            </RowCenter>
          </div>
        </React.Fragment>
      ),
    },
    {
      policy: (
      <p>{translate.t("organization.tabs.policies.policies.maxNumberAcceptations")}</p>
      ),
      recommended: (
      <p className={style.recommended}>{translate.t("organization.tabs.policies.recommended.numberAcceptations")}</p>
      ),
      value: (
        <Field
          component={Text}
          name="maxNumberAcceptations"
          type="text"
        />
      ),
    },
  ];

  const handleFormSubmit: (() => void) = (): void => {
    savePolicies();
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return(
    <React.StrictMode>
      <GenericForm
        name="orgPolicies"
        onSubmit={handleFormSubmit}
        initialValues={{
          maxAcceptanceDays: _.isNull(data.organization.maxAcceptanceDays)
                              ? ""
                              : data.organization.maxAcceptanceDays.toString(),
          maxAcceptanceSeverity: parseFloat(data.organization.maxAcceptanceSeverity)
                                  .toFixed(1)
                                  .toString(),
          maxNumberAcceptations: _.isNull(data.organization.maxNumberAcceptations)
                                  ? ""
                                  : data.organization.maxNumberAcceptations.toString(),
          minAcceptanceSeverity: parseFloat(data.organization.minAcceptanceSeverity)
                                  .toFixed(1)
                                  .toString(),
        }}
      >
        {({ handleSubmit, pristine, valid }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <DataTableNext
              bordered={true}
              dataset={policiesDataSet}
              exportCsv={false}
              headers={tableHeaders}
              id="policiesTbl"
              pageSize={5}
              search={false}
              striped={true}
            />
            <Can do="backend_api_mutations_update_organization_policies_mutate">
              {pristine || loadingPolicies || savingPolicies ? undefined : (
                <ButtonToolbar>
                  <Button onClick={handleSubmit}>
                    {translate.t("organization.tabs.policies.save")}
                  </Button>
                </ButtonToolbar>

              )}
            </Can>
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { organizationPolicies as OrganizationPolicies };
