import { Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import {
  computeConfirmationMessage,
  isDowngrading,
  isDowngradingServices,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/businessLogic";
import type {
  IFormData,
  IServicesDataSet,
  IServicesFormProps,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
  Well,
} from "styles/styledComponents";
import { FormikDropdown, FormikText, FormikTextArea } from "utils/forms/fields";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const downgradeReasons: string[] = [
  "NONE",
  "GROUP_SUSPENSION",
  "GROUP_FINALIZATION",
  "BUDGET",
  "OTHER",
];

const MAX_LENGTH_VALIDATOR = 250;
const maxLength250 = maxLength(MAX_LENGTH_VALIDATOR);

const ServicesForm: React.FC<IServicesFormProps> = (
  props: IServicesFormProps
): JSX.Element => {
  const {
    groupName,
    isModalOpen,
    submittingGroupData,
    setIsModalOpen,
    data,
    loadingGroupData,
  } = props;
  const { values, setFieldValue, dirty, submitForm, isValid } =
    useFormikContext<IFormData>();

  const handleMachineBtnChange: (withMachine: boolean) => void = (
    withMachine: boolean
  ): void => {
    setFieldValue("machine", withMachine);
    if (!withMachine) {
      setFieldValue("squad", false);
    }
  };

  const handleSquadBtnChange: (withSquad: boolean) => void = (
    withSquad: boolean
  ): void => {
    setFieldValue("squad", withSquad);
    if (withSquad) {
      setFieldValue("machine", true);
    }
  };

  const handleClose: () => void = useCallback((): void => {
    setIsModalOpen(false);
  }, [setIsModalOpen]);
  const handleTblButtonClick: () => void = useCallback((): void => {
    setIsModalOpen(true);
  }, [setIsModalOpen]);

  // Rendered elements
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "service",
      header: translate.t("searchFindings.servicesTable.service"),
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "status",
      header: translate.t("searchFindings.servicesTable.status"),
      width: "25%",
      wrapped: true,
    },
  ];
  const servicesList: IServicesDataSet[] = [
    {
      id: "machineSwitch",
      onChange: handleMachineBtnChange,
      service: "machine",
    },
    {
      id: "squadSwitch",
      onChange: handleSquadBtnChange,
      service: "squad",
    },
  ];

  const servicesDataSet: Record<string, JSX.Element>[] = [
    {
      service: <p>{translate.t("searchFindings.servicesTable.type")}</p>,
      status: (
        <Field component={FormikDropdown} name={"type"}>
          <option value={"CONTINUOUS"}>
            {translate.t("searchFindings.servicesTable.continuous")}
          </option>
          <option value={"ONESHOT"}>
            {translate.t("searchFindings.servicesTable.oneShot")}
          </option>
        </Field>
      ),
    },
    {
      service: <p>{translate.t("searchFindings.servicesTable.service")}</p>,
      status: (
        <Field component={FormikDropdown} name={"service"}>
          <option value={"BLACK"}>
            {translate.t("searchFindings.servicesTable.black")}
          </option>
          <option value={"WHITE"}>
            {translate.t("searchFindings.servicesTable.white")}
          </option>
        </Field>
      ),
    },
  ].concat(
    servicesList.map(
      (
        element: IServicesDataSet
      ): {
        service: JSX.Element;
        status: JSX.Element;
      } => ({
        service: (
          <p>
            {translate.t(`searchFindings.servicesTable.${element.service}`)}
          </p>
        ),
        status: (
          <FormGroup>
            <Field
              component={FormikSwitchButton}
              id={element.id}
              name={element.service}
              offlabel={translate.t("searchFindings.servicesTable.inactive")}
              onChange={
                _.isUndefined(element.onChange) ? undefined : element.onChange
              }
              onlabel={translate.t("searchFindings.servicesTable.active")}
              type={"checkbox"}
            />
          </FormGroup>
        ),
      })
    )
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <Form id={"editGroup"}>
      <DataTableNext
        bordered={true}
        dataset={servicesDataSet}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblServices"}
        pageSize={10}
        search={false}
        striped={true}
      />
      {/* Intentionally hidden while loading/submitting to offer a better UX
       *   this way the button does not twinkle and is visually stable
       */}
      {!dirty || loadingGroupData || submittingGroupData ? undefined : (
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={handleTblButtonClick}>
                {translate.t("searchFindings.servicesTable.modal.continue")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      )}
      <Modal
        headerTitle={translate.t("searchFindings.servicesTable.modal.title")}
        open={isModalOpen}
      >
        <ControlLabel>
          {translate.t("searchFindings.servicesTable.modal.changesToApply")}
        </ControlLabel>
        <Well>
          {computeConfirmationMessage(data, values).map(
            (line: string): JSX.Element => (
              <p key={line}>{line}</p>
            )
          )}
        </Well>
        <FormGroup>
          <ControlLabel>
            {translate.t("searchFindings.servicesTable.modal.observations")}
          </ControlLabel>
          <Field
            component={FormikTextArea}
            name={"comments"}
            placeholder={translate.t(
              "searchFindings.servicesTable.modal.observationsPlaceholder"
            )}
            type={"text"}
            validate={composeValidators([validTextField, maxLength250])}
          />
        </FormGroup>
        {isDowngradingServices(data, values) ? (
          <FormGroup>
            <ControlLabel>
              {translate.t("searchFindings.servicesTable.modal.downgrading")}
            </ControlLabel>
            <Field component={FormikDropdown} name={"reason"} type={"text"}>
              {downgradeReasons.map(
                (reason: string): JSX.Element => (
                  <option key={reason} value={reason}>
                    {translate.t(
                      `searchFindings.servicesTable.modal.${_.camelCase(
                        reason.toLowerCase()
                      )}`
                    )}
                  </option>
                )
              )}
            </Field>
          </FormGroup>
        ) : undefined}
        {isDowngrading(true, values.asm) ? (
          <FormGroup>
            <ControlLabel>
              {translate.t("searchFindings.servicesTable.modal.warning")}
            </ControlLabel>
            <Alert>
              {translate.t(
                "searchFindings.servicesTable.modal.warningDowngradeASM"
              )}
            </Alert>
          </FormGroup>
        ) : undefined}
        <FormGroup>
          <ControlLabel>
            {translate.t("searchFindings.servicesTable.modal.typeGroupName")}
          </ControlLabel>
          <Field
            component={FormikText}
            name={"confirmation"}
            placeholder={groupName.toLowerCase()}
            type={"text"}
            validate={required}
          />
        </FormGroup>
        <Alert>
          {"* "}
          {translate.t(
            "organization.tabs.groups.newGroup.extraChargesMayApply"
          )}
        </Alert>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={handleClose}>
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button disabled={!isValid} onClick={submitForm} type={"submit"}>
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </Form>
  );
};

export { ServicesForm };
