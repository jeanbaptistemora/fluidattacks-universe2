import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Grid, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { useParams } from "react-router";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeaderConfig } from "../../../../components/DataTableNext/types";
import { Can } from "../../../../utils/authz/Can";
import { Text } from "../../../../utils/forms/fields";
import { Logger } from "../../../../utils/logger";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import { translate } from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";
import { default as style } from "./index.css";
import { GET_ORGANIZATION_POLICIES, UPDATE_ORGANIZATION_POLICIES } from "./queries";
import { IOrganizationPolicies, IPoliciesFormData } from "./types";

const organizationPolicies: React.FC<IOrganizationPolicies> = (props: IOrganizationPolicies): JSX.Element => {

  // State management
  const { organizationId } = props;
  const { organizationName } = useParams();
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
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "value",
      header: translate.t("organization.tabs.policies.value"),
      width: "25%",
      wrapped: true,
    },
  ];

  const policiesDataSet: Array<Record<string, JSX.Element>> = [
    {
      policy: (
      <p>{translate.t("organization.tabs.policies.policies.maxAcceptanceDays")}</p>
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
      value: (
        <React.Fragment>
          <Grid className={style.severityGrid} fluid={true}>
            <Row className={style.severityRow}>
              <Col md={5} lg={5}>
                <Field
                  component={Text}
                  name="minAcceptanceSeverity"
                  type="text"
                />
              </Col>
              <Col md={2} lg={2}>
                <p>-</p>
              </Col>
              <Col md={5} lg={5}>
                <Field
                  component={Text}
                  name="maxAcceptanceSeverity"
                  type="text"
                />
              </Col>
            </Row>
          </Grid>
        </React.Fragment>
      ),
    },
    {
      policy: (
      <p>{translate.t("organization.tabs.policies.policies.maxNumberAcceptations")}</p>
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
            <Can do="backend_api_resolvers_organization__do_update_organization_policies">
              {pristine || loadingPolicies || savingPolicies ? undefined : (
                <ButtonToolbar className="pull-right">
                  <Button bsStyle="success" onClick={handleSubmit}>
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
