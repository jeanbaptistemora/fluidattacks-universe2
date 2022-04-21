import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import type { Moment } from "moment";
import React from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { GET_ROOTS } from "../../GroupScopeView/queries";
import type { Root } from "../../GroupScopeView/types";
import { AffectedReattackAccordion } from "../AffectedReattackAccordion";
import { GET_REATTACK_VULNS } from "../AffectedReattackAccordion/queries";
import type {
  IFinding,
  IFindingsQuery,
} from "../AffectedReattackAccordion/types";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import globalStyle from "styles/global.css";
import {
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import {
  FormikAutocompleteText,
  FormikCheckbox,
  FormikDateTime,
  FormikDropdown,
  FormikFileInput,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import {
  composeValidators,
  dateTimeBeforeToday,
  isValidFileSize,
  maxLength,
  numeric,
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
  blockingHours: number;
  accessibility: string[];
  affectedComponents: string[];
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

  const { data: findingsData } = useQuery<IFindingsQuery>(GET_REATTACK_VULNS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load reattack vulns", error);
      });
    },
    variables: { groupName },
  });
  const findings =
    findingsData === undefined ? [] : findingsData.group.findings;
  const hasReattacks = findings.some(
    (finding: IFinding): boolean => finding.vulnerabilitiesToReattack.length > 0
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
          blockingHours: 0,
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
        {({ dirty, isSubmitting, values }): JSX.Element => (
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
                    <option value={"CLIENT_APPROVES_CHANGE_TOE"}>
                      {t("group.events.form.type.toeChange")}
                    </option>
                    <option value={"CLIENT_DETECTS_ATTACK"}>
                      {t("group.events.form.type.detectsAttack")}
                    </option>
                    <option value={"HIGH_AVAILABILITY_APPROVAL"}>
                      {t("group.events.form.type.highAvailability")}
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
                </FormGroup>
              </Col50>
            </Row>
            {values.eventType === "INCORRECT_MISSING_SUPPLIES" ? (
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.blockingHours")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      name={"blockingHours"}
                      type={"number"}
                      validate={composeValidators([numeric, required])}
                    />
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {t("group.events.form.components.title")}
                    </ControlLabel>
                    <br />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.fluidStation")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"FLUID_STATION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.clientStation")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"CLIENT_STATION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.toeExclusion")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"TOE_EXCLUSSION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.documentation")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"DOCUMENTATION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.localConn")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"LOCAL_CONNECTION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.internetConn")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"INTERNET_CONNECTION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.vpnConn")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"VPN_CONNECTION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.toeLocation")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"TOE_LOCATION"}
                    />
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
                      label={t("group.events.form.components.testData")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"TEST_DATA"}
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
                      label={t("group.events.form.components.toeUnaccessible")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"TOE_UNACCESSIBLE"}
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
                      label={t("group.events.form.components.toeAlteration")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"TOE_ALTERATION"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.sourceCode")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"SOURCE_CODE"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.components.compileError")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"COMPILE_ERROR"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={t("group.events.form.other")}
                      name={"affectedComponents"}
                      type={"checkbox"}
                      value={"OTHER"}
                    />
                  </FormGroup>
                </Col50>
              </Row>
            ) : undefined}
            <Row>
              <Col100>
                <FormGroup>
                  <ControlLabel>{t("group.events.form.details")}</ControlLabel>
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
                  <ControlLabel>{t("group.events.form.evidence")}</ControlLabel>
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
                    validate={composeValidators([validEventFile, maxFileSize])}
                  />
                </FormGroup>
              </Col50>
            </Row>
            {hasReattacks ? (
              <FormGroup>
                <ControlLabel>
                  {t("group.events.form.affectedReattacks.sectionTitle")}
                </ControlLabel>
                <br />
                <Field
                  component={FormikCheckbox}
                  label={t("group.events.form.affectedReattacks.checkbox")}
                  name={"affectsReattacks"}
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
            <ModalFooter>
              <Button onClick={onClose} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Button
                disabled={!dirty || isSubmitting}
                type={"submit"}
                variant={"primary"}
              >
                {t("confirmmodal.proceed")}
              </Button>
            </ModalFooter>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { IFormValues, AddModal };
