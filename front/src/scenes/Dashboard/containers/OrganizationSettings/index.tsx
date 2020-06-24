import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { useLocation } from "react-router";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";
import { GET_ORGANIZATION_SETTINGS } from "./queries";

const organizationSettings: React.FC = (): JSX.Element => {
  const { state } = useLocation<{ organizationId: string }>();
  const organizationId: string = state.organizationId;

  const { data, loading: loadingSettings, refetch: refetchSettings } = useQuery(GET_ORGANIZATION_SETTINGS, {
    onError: (error: ApolloError): void => {
      handleGraphQLErrors("An error occurred fetching organization settings", error);
    },
    variables: { organizationId },
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
          type="text"
        />
      ),
    },
    {
      rule: (
      <p>{translate.t("organization.tabs.settings.rules.acceptanceSeverityRange")}</p>
      ),
      value: (
        <Field
          component={textField}
          type="text"
        />
      ),
    },
    {
      rule: (
      <p>{translate.t("organization.tabs.settings.rules.maxNumberAcceptations")}</p>
      ),
      value: (
        <Field
          component={textField}
          type="text"
        />
      ),
    },
  ];

  const saveSettings: (() => void) = (): void => {
    const submit: boolean = true;
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return(
    <React.StrictMode>
      <GenericForm
        name="orgSettings"
        onSubmit={saveSettings}
        initialValues={{
          maxAcceptanceDays: data.organization.maxAcceptanceDays,
          maxAcceptanceSeverity: data.organization.maxAcceptanceSeverity,
          maxNumberAcceptations: data.organization.maxNumberAcceptations,
          minAcceptanceSeverity: data.organization.minAcceptanceSeverity,
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
            {pristine || loadingSettings ? undefined : (
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
