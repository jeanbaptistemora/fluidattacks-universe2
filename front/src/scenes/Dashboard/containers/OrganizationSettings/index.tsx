import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";

const organizationSettings: React.FC = (): JSX.Element => {

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

  return(
    <GenericForm
      name="orgSettings"
      onSubmit={saveSettings}
      initialValues={{
        maxAcceptanceDays: 0,
        maxAcceptanceSeverity: 10,
        minAcceptanceSeverity: 0,
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
          {pristine ? undefined : (
            <ButtonToolbar className="pull-right">
              <Button bsStyle="success" onClick={handleSubmit}>
                {translate.t("organization.tabs.settings.save")}
              </Button>
            </ButtonToolbar>
          )}
        </React.Fragment>
      )}
    </GenericForm>
    );
};

export { organizationSettings as OrganizationSettings };
