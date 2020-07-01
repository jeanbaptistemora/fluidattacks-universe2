import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { useSelector } from "react-redux";
import { useLocation, useParams } from "react-router";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { textField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";
import { GET_ORGANIZATION_SETTINGS, UPDATE_ORGANIZATION_SETTINGS } from "./queries";
import { ILocationState, ISettingsFormData } from "./types";

const organizationSettings: React.FC = (): JSX.Element => {

  // State management
  const { organizationName } = useParams();
  const location: ILocationState = useLocation<{ organizationId: string }>();
  const selector: (state: {}, ...fields: string[]) => ISettingsFormData = formValueSelector("orgSettings");
  const formValues: ISettingsFormData = useSelector((state: {}) =>
    selector(state, "maxAcceptanceDays", "maxAcceptanceSeverity", "maxNumberAcceptations", "minAcceptanceSeverity"));

  let identifier: string = organizationName;
  if (!_.isUndefined(location.state)) {
    identifier = location.state.organizationId;
  }

  // GraphQL Operations
  const { data, loading: loadingSettings } = useQuery(GET_ORGANIZATION_SETTINGS, {
    onError: (error: ApolloError): void => {
      handleGraphQLErrors("An error occurred fetching organization settings", error);
    },
    variables: { identifier },
  });

  const [saveSettings, { loading: savingSettings }] = useMutation(UPDATE_ORGANIZATION_SETTINGS, {
    onCompleted: (): void => {
      mixpanel.track("UpdateOrganizationSettings", formValues);
      msgSuccess(
        translate.t("organization.tabs.settings.success"),
        translate.t("organization.tabs.settings.success_title"),
      );
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        let msg: string;

        switch (message) {
          case "Exception - Acceptance days should be zero or positive":
            msg = "organization.tabs.settings.errors.maxAcceptanceDays";
            break;
          case "Exception - Severity value should be a positive floating number between 0.0 a 10.0":
            msg = "organization.tabs.settings.errors.acceptanceSeverity";
            break;
          case "Exception - Min acceptance severity value should not be higher than the max value":
            msg = "organization.tabs.settings.errors.acceptanceSeverityRange";
            break;
          case "Exception - Number of acceptations should be zero or positive":
            msg = "organization.tabs.settings.errors.maxNumberAcceptations";
            break;
          default:
            msg = "group_alerts.error_textsad";
            rollbar.error("An error occurred updating the organization settings", error);
        }
        msgError(translate.t(msg));
      });
    },
    variables: {
      identifier,
      maxAcceptanceDays: parseInt(formValues.maxAcceptanceDays, 10),
      maxAcceptanceSeverity: parseFloat(formValues.maxAcceptanceSeverity),
      maxNumberAcceptations: parseInt(formValues.maxNumberAcceptations, 10),
      minAcceptanceSeverity: parseFloat(formValues.minAcceptanceSeverity),
    },
  });

  const tableHeaders: IHeader[] = [
    {
      dataField: "rule",
      header: translate.t("organization.tabs.settings.rule"),
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "value",
      header: translate.t("organization.tabs.settings.value"),
      width: "25%",
      wrapped: true,
    },
  ];

  const settingsDataSet: Array<Record<string, JSX.Element>> = [
    {
      rule: (
      <p>{translate.t("organization.tabs.settings.rules.maxAcceptanceDays")}</p>
      ),
      value: (
        <Field
          component={textField}
          name="maxAcceptanceDays"
          type="text"
        />
      ),
    },
    {
      rule: (
      <p>{translate.t("organization.tabs.settings.rules.acceptanceSeverityRange")}</p>
      ),
      value: (
        <React.Fragment>
          <Field
            component={textField}
            name="minAcceptanceSeverity"
            type="text"
          />
          <p> - </p>
          <Field
            component={textField}
            name="maxAcceptanceSeverity"
            type="text"
          />
        </React.Fragment>
      ),
    },
    {
      rule: (
      <p>{translate.t("organization.tabs.settings.rules.maxNumberAcceptations")}</p>
      ),
      value: (
        <Field
          component={textField}
          name="maxNumberAcceptations"
          type="text"
        />
      ),
    },
  ];

  const handleFormSubmit: (() => void) = (): void => {
    saveSettings();
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return(
    <React.StrictMode>
      <GenericForm
        name="orgSettings"
        onSubmit={handleFormSubmit}
        initialValues={{
          maxAcceptanceDays: _.isNull(data.organization.maxAcceptanceDays)
                              ? ""
                              : data.organization.maxAcceptanceDays.toString(),
          maxAcceptanceSeverity: data.organization.maxAcceptanceSeverity.toString(),
          maxNumberAcceptations: _.isNull(data.organization.maxNumberAcceptations)
                                  ? ""
                                  : data.organization.maxNumberAcceptations.toString(),
          minAcceptanceSeverity: data.organization.minAcceptanceSeverity.toString(),
        }}
      >
        {({ handleSubmit, pristine, valid }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <DataTableNext
              bordered={true}
              dataset={settingsDataSet}
              exportCsv={false}
              headers={tableHeaders}
              id="settingsTbl"
              pageSize={5}
              remote={false}
              search={false}
              striped={true}
            />
            {pristine || loadingSettings || savingSettings ? undefined : (
              <ButtonToolbar className="pull-right">
                <Button bsStyle="success" onClick={handleSubmit}>
                  {translate.t("organization.tabs.settings.save")}
                </Button>
              </ButtonToolbar>
            )}
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { organizationSettings as OrganizationSettings };
