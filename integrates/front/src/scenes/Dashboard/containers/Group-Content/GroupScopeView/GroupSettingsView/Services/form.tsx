import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { Input, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Switch } from "components/Switch";
import { Text } from "components/Text";
import {
  computeConfirmationMessage,
  isDowngrading,
  isDowngradingServices,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services/businessLogic";
import type {
  IFormData,
  IServicesFormProps,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services/types";
import { FormGroup } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";
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
  const { t } = useTranslation();

  const handleMachineBtnChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const withMachine = event.target.checked;
      setFieldValue("machine", withMachine);
      if (!withMachine) {
        setFieldValue("squad", false);
      }
    },
    [setFieldValue]
  );

  const handleSquadBtnChange: (withSquad: boolean) => void = useCallback(
    (withSquad: boolean): void => {
      setFieldValue("squad", withSquad);
      if (withSquad) {
        setFieldValue("machine", true);
      }
    },
    [setFieldValue]
  );

  const handleClose: () => void = useCallback((): void => {
    setIsModalOpen(false);
  }, [setIsModalOpen]);
  const handleTblButtonClick: () => void = useCallback((): void => {
    setIsModalOpen(true);
  }, [setIsModalOpen]);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateGroupServices: boolean = permissions.can(
    "api_mutations_update_group_mutate"
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <Form id={"editGroup"}>
      <Row>
        <Col lg={30} md={50} sm={50}>
          <Card>
            <Select
              disabled={!canUpdateGroupServices}
              label={t("searchFindings.servicesTable.type")}
              name={"type"}
            >
              <option value={"CONTINUOUS"}>
                {t("searchFindings.servicesTable.continuous")}
              </option>
              <option value={"ONESHOT"}>
                {t("searchFindings.servicesTable.oneShot")}
              </option>
            </Select>
          </Card>
        </Col>
        <Col lg={30} md={50} sm={50}>
          <Card>
            <Select
              disabled={!canUpdateGroupServices}
              label={t("searchFindings.servicesTable.service")}
              name={"service"}
            >
              <option value={"BLACK"}>
                {t("searchFindings.servicesTable.black")}
              </option>
              <option value={"WHITE"}>
                {t("searchFindings.servicesTable.white")}
              </option>
            </Select>
          </Card>
        </Col>
        <Col lg={20} md={50} sm={50}>
          <Card>
            <Text mb={2}>{t("searchFindings.servicesTable.machine")}</Text>
            <Switch
              checked={values.machine}
              disabled={!canUpdateGroupServices}
              label={{
                off: t("searchFindings.servicesTable.inactive"),
                on: t("searchFindings.servicesTable.active"),
              }}
              name={"machine"}
              onChange={handleMachineBtnChange}
            />
          </Card>
        </Col>
        <Col lg={20} md={50} sm={50}>
          <Card>
            <Text mb={2}>{t("searchFindings.servicesTable.squad")}</Text>
            <Field
              component={FormikSwitchButton}
              disabled={!canUpdateGroupServices}
              id={"squadSwitch"}
              name={"squad"}
              offlabel={t("searchFindings.servicesTable.inactive")}
              onChange={handleSquadBtnChange}
              onlabel={t("searchFindings.servicesTable.active")}
              type={"checkbox"}
            />
          </Card>
        </Col>
      </Row>
      {/* Intentionally hidden while loading/submitting to offer a better UX
       *   this way the button does not twinkle and is visually stable
       */}
      {!dirty || loadingGroupData || submittingGroupData ? undefined : (
        <div className={"mt2"}>
          <Button onClick={handleTblButtonClick} variant={"secondary"}>
            {t("searchFindings.servicesTable.modal.continue")}
          </Button>
        </div>
      )}
      <Modal
        open={isModalOpen}
        title={t("searchFindings.servicesTable.modal.title")}
      >
        <Text mb={2}>
          {t("searchFindings.servicesTable.modal.changesToApply")}
        </Text>
        <div className={"mb3 ml4"}>
          {computeConfirmationMessage(data, values).map(
            (line: string): JSX.Element => (
              <p key={line}>{line}</p>
            )
          )}
        </div>
        <FormGroup>
          <TextArea
            label={t("searchFindings.servicesTable.modal.observations")}
            name={"comments"}
            placeholder={t(
              "searchFindings.servicesTable.modal.observationsPlaceholder"
            )}
            validate={composeValidators([validTextField, maxLength250])}
          />
        </FormGroup>
        {isDowngradingServices(data, values) ? (
          <FormGroup>
            <Select
              label={t("searchFindings.servicesTable.modal.downgrading")}
              name={"reason"}
            >
              {downgradeReasons.map(
                (reason: string): JSX.Element => (
                  <option key={reason} value={reason}>
                    {t(
                      `searchFindings.servicesTable.modal.${_.camelCase(
                        reason.toLowerCase()
                      )}`
                    )}
                  </option>
                )
              )}
            </Select>
          </FormGroup>
        ) : undefined}
        {isDowngrading(true, values.asm) ? (
          <FormGroup>
            <Text mb={2}>
              {t("searchFindings.servicesTable.modal.warning")}
            </Text>
            <Alert>
              {t("searchFindings.servicesTable.modal.warningDowngrade")}
            </Alert>
          </FormGroup>
        ) : undefined}
        <FormGroup>
          <Input
            label={t("searchFindings.servicesTable.modal.typeGroupName")}
            name={"confirmation"}
            placeholder={groupName.toLowerCase()}
            type={"text"}
            validate={required}
          />
        </FormGroup>
        <Alert>
          {"* "}
          {t("organization.tabs.groups.newGroup.extraChargesMayApply")}
        </Alert>
        <ModalConfirm
          disabled={!isValid}
          onCancel={handleClose}
          onConfirm={submitForm}
        />
      </Modal>
    </Form>
  );
};

export { ServicesForm };
