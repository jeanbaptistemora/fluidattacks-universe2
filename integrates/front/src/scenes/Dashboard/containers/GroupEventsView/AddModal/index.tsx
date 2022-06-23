import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
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
import globalStyle from "styles/global.css";
import {
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { authzGroupContext } from "utils/authz/config";
import {
  FormikAutocompleteText,
  FormikCheckbox,
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

interface IFormValues {
  eventDate: Moment | string;
  accessibility: string[];
  affectedComponents: string[];
  affectsReattacks: boolean;
  affectedReattacks: string[];
  eventType: string;
  detail: string;
  file?: FileList;
  image?: FileList;
  rootId: string;
  rootNickname: string;
}

interface IAddModalProps {
  groupName: string;
  onClose: () => void;
  onSubmit: (values: IFormValues) => Promise<void>;
}

const AddModal: React.FC<IAddModalProps> = ({
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
      rootId: roots[nicknames.indexOf(values.rootNickname)].id,
    });
  }

  const validations = object().shape({
    accessibility: array().min(1, t("validations.someRequired")),
    affectedComponents: array().when("eventType", {
      is: "INCORRECT_MISSING_SUPPLIES",
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
    affectedReattacks: array().when("affectsReattacks", {
      is: true,
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
    rootNickname: string().required().oneOf(nicknames, t("validations.oneOf")),
  });

  return (
    <Modal onClose={onClose} open={true} title={t("group.events.new")}>
      <Formik
        initialValues={{
          accessibility: [],
          affectedComponents: [],
          affectedReattacks: [],
          affectsReattacks: false,
          detail: "",
          eventDate: "",
          eventType: "",
          file: undefined,
          image: undefined,
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
                <Col50>
                  <FormGroup>
                    <ControlLabel>{t("group.events.form.date")}</ControlLabel>
                    <Field
                      component={FormikDateTime}
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
                    <ControlLabel>
                      {t("group.events.form.type.title")}
                    </ControlLabel>
                    <Field
                      component={FormikDropdown}
                      name={"eventType"}
                      validate={required}
                    >
                      <option value={""} />
                      <option value={"AUTHORIZATION_SPECIAL_ATTACK"}>
                        {t("group.events.form.type.specialAttack")}
                      </option>
                      <option value={"DATA_UPDATE_REQUIRED"}>
                        {t("group.events.form.type.dataUpdate")}
                      </option>
                      <option value={"INCORRECT_MISSING_SUPPLIES"}>
                        {t("group.events.form.type.missingSupplies")}
                      </option>
                      <option value={"TOE_DIFFERS_APPROVED"}>
                        {t("group.events.form.type.toeDiffers")}
                      </option>
                      <option value={"OTHER"}>
                        {t("group.events.form.other")}
                      </option>
                    </Field>
                  </FormGroup>
                </Col50>
              </Row>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.accessibility.title")}
                    </ControlLabel>
                    <br />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.accessibility.environment")}
                      name={"accessibility"}
                      type={"checkbox"}
                      value={"environment"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.accessibility.repository")}
                      name={"accessibility"}
                      type={"checkbox"}
                      value={"repository"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.accessibility.vpnConnection")}
                      name={"accessibility"}
                      type={"checkbox"}
                      value={"vpn_connection"}
                    />
                  </FormGroup>
                </Col50>
                {values.eventType === "INCORRECT_MISSING_SUPPLIES" ? (
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {t("group.events.form.components.title")}
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikCheckbox}
                        label={t("group.events.form.components.toeCredentials")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_CREDENTIALS"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={t("group.events.form.components.toePrivileges")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_PRIVILEGES"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={t("group.events.form.components.toeUnstability")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_UNSTABLE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={t("group.events.form.components.toeUnavailable")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_UNAVAILABLE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={t("group.events.form.components.testData")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TEST_DATA"}
                      />
                    </FormGroup>
                  </Col50>
                ) : undefined}
              </Row>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.details")}
                    </ControlLabel>
                    <Field
                      // eslint-disable-next-line react/forbid-component-props
                      className={globalStyle.noResize}
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
                      id={"image"}
                      name={"image"}
                      validate={composeValidators([
                        validEvidenceImage,
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
                      id={"file"}
                      name={"file"}
                      validate={composeValidators([
                        validEventFile,
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
