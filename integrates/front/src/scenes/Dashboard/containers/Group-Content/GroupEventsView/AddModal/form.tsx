import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import type { FieldValidator } from "formik";
import { Field, Form } from "formik";
import type { GraphQLError } from "graphql";
import React, { useCallback, useContext } from "react";
import { useTranslation } from "react-i18next";

import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import { GET_VERIFIED_FINDING_INFO } from "../AffectedReattackAccordion/queries";
import type {
  IFinding,
  IFindingsQuery,
} from "../AffectedReattackAccordion/types";
import { InputDateTime, InputFile, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { authzGroupContext } from "utils/authz/config";
import { castEventType } from "utils/formatHelpers";
import { FormikAutocompleteText } from "utils/forms/fields";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";
import { Logger } from "utils/logger";
import {
  composeValidators,
  dateTimeBeforeToday,
  isValidAmountOfFiles,
  isValidEvidenceName,
  isValidFileSize,
  maxLength,
  required,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validTextField,
} from "utils/validations";

const MAX_EVENT_DETAILS_LENGTH = 300;
const maxEventDetailsLength = maxLength(MAX_EVENT_DETAILS_LENGTH);

const MAX_FILE_SIZE = 10;
const maxFileSize = isValidFileSize(MAX_FILE_SIZE);
const MAX_AMOUNT_OF_FILES = 6;
const maxAmountOfFiles = isValidAmountOfFiles(MAX_AMOUNT_OF_FILES);

interface IAddModalFormProps {
  dirty: boolean;
  isSubmitting: boolean;
  values: {
    affectedReattacks: never[];
    affectsReattacks: boolean;
    detail: string;
    eventDate: string;
    eventType: string;
    files: undefined;
    images: undefined;
    rootId: string;
    rootNickname: string;
  };
  setFieldValue: (
    field: string,
    value: boolean,
    shouldValidate?: boolean | undefined
  ) => void;
  nicknames: string[];
  groupName: string;
  onClose: () => void;
  organizationName: string;
}

export const AddModalForm: React.FC<IAddModalFormProps> = ({
  dirty,
  isSubmitting,
  values,
  setFieldValue,
  nicknames,
  organizationName,
  groupName,
  onClose,
}: IAddModalFormProps): JSX.Element => {
  const { t } = useTranslation();

  const { data: findingsData } = useQuery<IFindingsQuery>(
    GET_VERIFIED_FINDING_INFO,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load reattack vulns", error);
        });
      },
      variables: { groupName },
    }
  );

  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const findings =
    findingsData === undefined ? [] : findingsData.group.findings;
  const canOnHold: boolean = attributes.can("can_report_vulnerabilities");
  const hasReattacks = findings.some(
    (finding: IFinding): boolean => !finding.verified
  );

  const validEvidenceName: FieldValidator = isValidEvidenceName(
    organizationName,
    groupName
  );

  const handleAffectsReattacksBtnChange = useCallback(
    (switchValue: boolean): void => {
      setFieldValue("affectsReattacks", switchValue);
    },
    [setFieldValue]
  );

  return (
    <Form>
      <Row>
        <Col>
          <InputDateTime
            label={t("group.events.form.date")}
            name={"eventDate"}
            validate={composeValidators([
              required,
              validDatetime,
              dateTimeBeforeToday,
            ])}
          />
        </Col>
        <Col>
          <FormGroup>
            <Select
              label={t("group.events.form.type")}
              name={"eventType"}
              validate={required}
            >
              <option value={""} />
              <option value={"AUTHORIZATION_SPECIAL_ATTACK"}>
                {t(castEventType("AUTHORIZATION_SPECIAL_ATTACK"))}
              </option>
              <option value={"CLIENT_EXPLICITLY_SUSPENDS_PROJECT"}>
                {t(castEventType("CLIENT_EXPLICITLY_SUSPENDS_PROJECT"))}
              </option>
              <option value={"CLONING_ISSUES"}>
                {t(castEventType("CLONING_ISSUES"))}
              </option>
              <option value={"CREDENTIAL_ISSUES"}>
                {t(castEventType("CREDENTIAL_ISSUES"))}
              </option>
              <option value={"DATA_UPDATE_REQUIRED"}>
                {t(castEventType("DATA_UPDATE_REQUIRED"))}
              </option>
              <option value={"ENVIRONMENT_ISSUES"}>
                {t(castEventType("ENVIRONMENT_ISSUES"))}
              </option>
              <option value={"INSTALLER_ISSUES"}>
                {t(castEventType("INSTALLER_ISSUES"))}
              </option>
              <option value={"MISSING_SUPPLIES"}>
                {t(castEventType("MISSING_SUPPLIES"))}
              </option>
              <option value={"NETWORK_ACCESS_ISSUES"}>
                {t(castEventType("NETWORK_ACCESS_ISSUES"))}
              </option>
              <option value={"OTHER"}>{t(castEventType("OTHER"))}</option>
              <option value={"REMOTE_ACCESS_ISSUES"}>
                {t(castEventType("REMOTE_ACCESS_ISSUES"))}
              </option>
              <option value={"TOE_DIFFERS_APPROVED"}>
                {t(castEventType("TOE_DIFFERS_APPROVED"))}
              </option>
              <option value={"VPN_ISSUES"}>
                {t(castEventType("VPN_ISSUES"))}
              </option>
            </Select>
          </FormGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <FormGroup>
            <ControlLabel>{t("group.events.form.root")}</ControlLabel>
            <Field
              component={FormikAutocompleteText}
              name={"rootNickname"}
              placeholder={t("group.events.form.rootPlaceholder")}
              suggestions={nicknames}
            />
          </FormGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <FormGroup>
            <TextArea
              label={t("group.events.form.details")}
              name={"detail"}
              validate={composeValidators([
                required,
                validTextField,
                maxEventDetailsLength,
              ])}
            />
          </FormGroup>
        </Col>
      </Row>
      <Row>
        <Col>
          <FormGroup>
            <InputFile
              accept={"image/png,video/webm"}
              id={"images"}
              label={t("group.events.form.evidence")}
              multiple={true}
              name={"images"}
              validate={composeValidators([
                validEvidenceImage,
                validEvidenceName,
                maxAmountOfFiles,
                maxFileSize,
              ])}
            />
          </FormGroup>
        </Col>
        <Col>
          <FormGroup>
            <InputFile
              accept={"application/pdf,application/zip,text/csv,text/plain"}
              id={"files"}
              label={t("group.events.form.evidenceFile")}
              name={"files"}
              validate={composeValidators([
                validEventFile,
                validEvidenceName,
                maxFileSize,
              ])}
            />
          </FormGroup>
        </Col>
      </Row>
      {hasReattacks && canOnHold ? (
        <FormGroup>
          <ControlLabel>
            {t("group.events.form.affectedReattacks.sectionTitle")}
          </ControlLabel>
          <br />
          {t("group.events.form.affectedReattacks.switchLabel")}
          <br />
          <Field
            component={FormikSwitchButton}
            name={"affectsReattacks"}
            offlabel={t("group.events.form.affectedReattacks.no")}
            onChange={handleAffectsReattacksBtnChange}
            onlabel={t("group.events.form.affectedReattacks.yes")}
            type={"checkbox"}
          />
          {values.affectsReattacks ? (
            <React.Fragment>
              <br />
              {t("group.events.form.affectedReattacks.selection")}
              <br />
              <br />
              <Row>
                <AffectedReattackAccordion findings={findings} />
              </Row>
            </React.Fragment>
          ) : undefined}
        </FormGroup>
      ) : undefined}
      <ModalConfirm disabled={!dirty || isSubmitting} onCancel={onClose} />
    </Form>
  );
};
