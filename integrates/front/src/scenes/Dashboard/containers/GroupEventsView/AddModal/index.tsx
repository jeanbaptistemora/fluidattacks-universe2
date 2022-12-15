import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import type { FieldValidator } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import type { Moment } from "moment";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { GET_ROOTS } from "../../GroupScopeView/queries";
import type { Root } from "../../GroupScopeView/types";
import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import { GET_VERIFIED_FINDING_INFO } from "../AffectedReattackAccordion/queries";
import type {
  IFinding,
  IFindingsQuery,
} from "../AffectedReattackAccordion/types";
import { Modal, ModalConfirm } from "components/Modal";
import {
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { authzGroupContext } from "utils/authz/config";
import { castEventType } from "utils/formatHelpers";
import {
  FormikAutocompleteText,
  FormikDateTime,
  FormikDropdown,
  FormikFileInput,
  FormikTextArea,
} from "utils/forms/fields";
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

interface IFormValues {
  eventDate: Moment | string;
  affectsReattacks: boolean;
  affectedReattacks: string[];
  eventType: string;
  detail: string;
  files?: FileList;
  images?: FileList;
  rootId: string;
  rootNickname: string;
}

interface IAddModalProps {
  groupName: string;
  organizationName: string;
  onClose: () => void;
  onSubmit: (values: IFormValues) => Promise<void>;
}

const AddModal: React.FC<IAddModalProps> = ({
  organizationName,
  groupName,
  onClose,
  onSubmit,
}: IAddModalProps): JSX.Element => {
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

  const { data } = useQuery<{ group: { roots: Root[] } }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
  });
  const roots =
    data === undefined
      ? []
      : data.group.roots.filter((root): boolean => root.state === "ACTIVE");
  const nicknames = roots.map((root): string => root.nickname);

  async function handleSubmit(values: IFormValues): Promise<void> {
    return onSubmit({
      ...values,
      rootId: values.rootNickname
        ? roots[nicknames.indexOf(values.rootNickname)].id
        : "",
    });
  }

  const validations = object().shape({
    affectedReattacks: array().when("affectsReattacks", {
      is: true,
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
    rootNickname: string()
      .oneOf(nicknames, t("validations.oneOf"))
      .when("eventType", {
        is: "MISSING_SUPPLIES",
        otherwise: string().required(),
        then: string().notRequired(),
      }),
  });

  const validEvidenceName: FieldValidator = isValidEvidenceName(
    organizationName,
    groupName
  );

  return (
    <Modal onClose={onClose} open={true} title={t("group.events.new")}>
      <Formik
        initialValues={{
          affectedReattacks: [],
          affectsReattacks: false,
          detail: "",
          eventDate: "",
          eventType: "",
          files: undefined,
          images: undefined,
          rootId: "",
          rootNickname: "",
        }}
        name={"newEvent"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting, values, setFieldValue }): JSX.Element => {
          function handleAffectsReattacksBtnChange(switchValue: boolean): void {
            setFieldValue("affectsReattacks", switchValue);
          }

          return (
            <Form>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>{t("group.events.form.date")}</ControlLabel>
                    <Field
                      component={FormikDateTime}
                      dataTestId={"event-date-time"}
                      name={"eventDate"}
                      validate={composeValidators([
                        required,
                        validDatetime,
                        dateTimeBeforeToday,
                      ])}
                    />
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>{t("group.events.form.type")}</ControlLabel>
                    <Field
                      component={FormikDropdown}
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
                      <option value={"OTHER"}>
                        {t(castEventType("OTHER"))}
                      </option>
                      <option value={"REMOTE_ACCESS_ISSUES"}>
                        {t(castEventType("REMOTE_ACCESS_ISSUES"))}
                      </option>
                      <option value={"TOE_DIFFERS_APPROVED"}>
                        {t(castEventType("TOE_DIFFERS_APPROVED"))}
                      </option>
                      <option value={"VPN_ISSUES"}>
                        {t(castEventType("VPN_ISSUES"))}
                      </option>
                    </Field>
                  </FormGroup>
                </Col50>
              </Row>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>{t("group.events.form.root")}</ControlLabel>
                    <Field
                      component={FormikAutocompleteText}
                      name={"rootNickname"}
                      placeholder={t("group.events.form.rootPlaceholder")}
                      suggestions={nicknames}
                    />
                  </FormGroup>
                </Col100>
              </Row>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.details")}
                    </ControlLabel>
                    <Field
                      // eslint-disable-next-line react/forbid-component-props
                      className={"noResize"}
                      component={FormikTextArea}
                      name={"detail"}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxEventDetailsLength,
                      ])}
                    />
                  </FormGroup>
                </Col100>
              </Row>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.evidence")}
                    </ControlLabel>
                    <Field
                      accept={"image/gif,image/png"}
                      component={FormikFileInput}
                      id={"images"}
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
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.evidenceFile")}
                    </ControlLabel>
                    <Field
                      accept={
                        "application/pdf,application/zip,text/csv,text/plain"
                      }
                      component={FormikFileInput}
                      id={"files"}
                      name={"files"}
                      validate={composeValidators([
                        validEventFile,
                        validEvidenceName,
                        maxFileSize,
                      ])}
                    />
                  </FormGroup>
                </Col50>
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
              <ModalConfirm
                disabled={!dirty || isSubmitting}
                onCancel={onClose}
              />
            </Form>
          );
        }}
      </Formik>
    </Modal>
  );
};

export type { IFormValues };
export { AddModal };
