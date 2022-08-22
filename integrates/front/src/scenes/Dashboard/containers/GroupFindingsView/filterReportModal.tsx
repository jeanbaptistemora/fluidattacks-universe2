import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import type { TestContext } from "yup";
import { array, number, object } from "yup";

import { Button } from "components/Button";
import { Col, Hr, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Tooltip } from "components/Tooltip";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { Col100 } from "styles/styledComponents";
import {
  FormikCheckbox,
  FormikDate,
  FormikDropdown,
  FormikText,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, isGreaterDate } from "utils/validations";

interface IDeactivationModalProps {
  isOpen: boolean;
  onClose: () => void;
  typesOptions: string[];
  closeReportsModal: () => void;
}

interface IFormValues {
  age: number | undefined;
  closingDate: string;
  findingTitle: string;
  maxSeverity: number | undefined;
  minSeverity: number | undefined;
  states: string[];
  treatments: string[];
  verifications: string[];
}

const FilterReportModal: React.FC<IDeactivationModalProps> = ({
  isOpen,
  onClose,
  typesOptions,
  closeReportsModal,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const formRef = useRef<FormikProps<IFormValues>>(null);
  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      onClose();
      closeReportsModal();
      setIsVerifyDialogOpen(false);
      msgSuccess(
        t("groupAlerts.reportRequested"),
        t("groupAlerts.titleSuccess")
      );
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - The user already has a requested report for the same group":
            msgError(t("groupAlerts.reportAlreadyRequested"));
            break;
          case "Exception - Stakeholder could not be verified":
            msgError(t("group.findings.report.alerts.nonVerifiedStakeholder"));
            break;
          case "Exception - The verification code is invalid":
            msgError(t("group.findings.report.alerts.invalidVerificationCode"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred requesting group report", error);
        }
      });
    },
  });

  const handleRequestGroupReport = useCallback(
    (
      age: number | undefined,
      closingDate: string | undefined,
      findingTitle: string | undefined,
      maxSeverity: number | undefined,
      minSeverity: number | undefined,
      states: string[],
      treatments: string[] | undefined,
      verifications: string[],
      verificationCode: string
    ): void => {
      const reportType = "XLS";
      mixpanel.track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          age,
          closingDate,
          findingTitle,
          groupName,
          maxSeverity,
          minSeverity,
          reportType,
          states,
          treatments,
          verificationCode,
          verifications,
        },
      });
    },
    [groupName, requestGroupReport]
  );

  const validations = object().shape({
    maxSeverity: number()
      .max(10)
      .test({
        exclusive: false,
        message: "Must be greater than or equal to Min severity",
        name: "min",
        params: {},
        test: (
          value: number | undefined,
          thisContext: TestContext
        ): boolean => {
          const { minSeverity } = thisContext.parent;

          return value === undefined || minSeverity === undefined
            ? true
            : value >= (minSeverity ?? 0);
        },
      }),
    minSeverity: number()
      .min(0)
      .test({
        exclusive: false,
        message: "Must be less than or equal to Max severity",
        name: "max",
        params: {},
        test: (
          value: number | undefined,
          thisContext: TestContext
        ): boolean => {
          const { maxSeverity } = thisContext.parent;

          return value === undefined || maxSeverity === undefined
            ? true
            : value <= (maxSeverity ?? 10);
        },
      }),
    states: array().min(1, t("validations.someRequired")),
    treatments: array().when("closingDate", {
      is: (closingDate: string): boolean => _.isEmpty(closingDate),
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
  });

  return (
    <React.StrictMode>
      <Modal
        minWidth={600}
        onClose={onClose}
        open={isOpen}
        title={t("group.findings.report.modalTitle")}
      >
        <Col100>
          <VerifyDialog isOpen={isVerifyDialogOpen}>
            {(setVerifyCallbacks): JSX.Element => {
              function onRequestReport(values: {
                age: number | undefined;
                closingDate: string;
                findingTitle: string;
                maxSeverity: number | undefined;
                minSeverity: number | undefined;
                states: string[];
                treatments: string[];
                verifications: string[];
              }): void {
                setVerifyCallbacks(
                  (verificationCode: string): void => {
                    handleRequestGroupReport(
                      _.isEmpty(String(values.age)) ? undefined : values.age,
                      _.isEmpty(values.closingDate)
                        ? undefined
                        : values.closingDate,
                      _.isEmpty(values.findingTitle)
                        ? undefined
                        : values.findingTitle,
                      _.isEmpty(String(values.maxSeverity))
                        ? undefined
                        : values.maxSeverity,
                      _.isEmpty(String(values.minSeverity))
                        ? undefined
                        : values.minSeverity,
                      values.states,
                      _.isEmpty(values.closingDate)
                        ? values.treatments
                        : undefined,
                      values.verifications,
                      verificationCode
                    );
                  },
                  (): void => {
                    setIsVerifyDialogOpen(false);
                  }
                );
                setIsVerifyDialogOpen(true);
              }

              return (
                <Formik
                  initialValues={{
                    age: undefined,
                    closingDate: "",
                    findingTitle: "",
                    maxSeverity: undefined,
                    minSeverity: undefined,
                    states: [],
                    treatments: [],
                    verifications: [],
                  }}
                  innerRef={formRef}
                  name={"reportTreatments"}
                  onSubmit={onRequestReport}
                  validationSchema={validations}
                >
                  {({ values }): JSX.Element => {
                    function onChangeDate(
                      event: React.ChangeEvent<HTMLInputElement>
                    ): void {
                      if (event.target.value !== "") {
                        formRef.current?.setFieldValue(
                          "states",
                          values.states.filter(
                            (state: string): boolean => state !== "OPEN"
                          )
                        );
                      }
                    }

                    return (
                      <Form>
                        <p className={"mb0"}>
                          {t("group.findings.report.filterReportDescription")}
                        </p>
                        <Row align={"start"} justify={"start"}>
                          <Col lg={50} md={50} sm={50}>
                            <p className={"mb1 mt1"}>
                              <span className={"fw8"}>
                                {t("group.findings.report.findingTitle.text")}
                              </span>
                            </p>
                            <Tooltip
                              id={"group.findings.report.findingTitle.id"}
                              place={"top"}
                              tip={t(
                                "group.findings.report.findingTitle.tooltip"
                              )}
                            >
                              <Field
                                component={FormikDropdown}
                                name={"findingTitle"}
                              >
                                <option value={""} />
                                {typesOptions.map(
                                  (typeCode: string): JSX.Element => (
                                    <option key={typeCode} value={typeCode}>
                                      {typeCode}
                                    </option>
                                  )
                                )}
                              </Field>
                            </Tooltip>
                          </Col>
                          <Col lg={30} md={30} sm={90}>
                            <Row align={"start"} justify={"between"}>
                              <Col lg={40} md={40} sm={40}>
                                <p className={"mb1 mt1"}>
                                  <span className={"fw8"}>
                                    {t(
                                      "group.findings.report.minSeverity.text"
                                    )}
                                  </span>
                                </p>
                                <Tooltip
                                  id={"group.findings.report.minSeverity.id"}
                                  place={"top"}
                                  tip={t(
                                    "group.findings.report.minSeverity.tooltip"
                                  )}
                                >
                                  <Field
                                    component={FormikText}
                                    max={10}
                                    min={0}
                                    name={"minSeverity"}
                                    step={0.1}
                                    type={"number"}
                                  />
                                </Tooltip>
                              </Col>
                              <Col lg={10} md={10} sm={50}>
                                <Row align={"center"} justify={"center"}>
                                  <Col lg={100} md={100} sm={50}>
                                    <FontAwesomeIcon
                                      // eslint-disable-next-line react/forbid-component-props
                                      className={"pt4"}
                                      color={"gray"}
                                      icon={faMinus}
                                    />
                                  </Col>
                                </Row>
                              </Col>
                              <Col lg={40} md={50} sm={50}>
                                <p className={"mb1 mt1"}>
                                  <span className={"fw8"}>
                                    {t(
                                      "group.findings.report.maxSeverity.text"
                                    )}
                                  </span>
                                </p>
                                <Tooltip
                                  id={"group.findings.report.maxSeverity.id"}
                                  place={"top"}
                                  tip={t(
                                    "group.findings.report.maxSeverity.tooltip"
                                  )}
                                >
                                  <Field
                                    component={FormikText}
                                    max={10}
                                    min={0}
                                    name={"maxSeverity"}
                                    step={0.1}
                                    type={"number"}
                                  />
                                </Tooltip>
                              </Col>
                            </Row>
                          </Col>
                          <Col lg={5} md={5} sm={5} />
                          <Col lg={15} md={15} sm={50}>
                            <p className={"mb1 mt1"}>
                              <span className={"fw8"}>
                                {t("group.findings.report.age.text")}
                              </span>
                            </p>
                            <Tooltip
                              id={"group.findings.report.age.id"}
                              place={"top"}
                              tip={t("group.findings.report.age.tooltip")}
                            >
                              <Field
                                component={FormikText}
                                max={10000}
                                min={0}
                                name={"age"}
                                type={"number"}
                              />
                            </Tooltip>
                          </Col>
                          <Col lg={90} md={90} sm={90}>
                            <Col lg={50} md={50} sm={50}>
                              <p className={"mb1 mt1"}>
                                <span className={"fw8"}>
                                  {t("group.findings.report.closingDate.text")}
                                </span>
                              </p>
                              <Tooltip
                                id={"group.findings.report.closingDate.id"}
                                place={"top"}
                                tip={t(
                                  "group.findings.report.closingDate.tooltip"
                                )}
                              >
                                <Field
                                  component={FormikDate}
                                  customChange={onChangeDate}
                                  name={"closingDate"}
                                  validate={composeValidators([isGreaterDate])}
                                />
                              </Tooltip>
                            </Col>
                          </Col>
                          {_.isEmpty(values.closingDate) ? (
                            <Col lg={50} md={50} sm={50}>
                              <p className={"mb1 mt1"}>
                                <span className={"fw8"}>
                                  {t("group.findings.report.treatment")}
                                </span>
                              </p>
                              {[
                                "ACCEPTED",
                                "ACCEPTED_UNDEFINED",
                                "IN_PROGRESS",
                                "NEW",
                              ].map(
                                (treatment): JSX.Element => (
                                  <Field
                                    component={FormikCheckbox}
                                    disabled={!_.isEmpty(values.closingDate)}
                                    key={treatment}
                                    label={t(
                                      `searchFindings.tabDescription.treatment.${_.camelCase(
                                        treatment
                                      )}`
                                    )}
                                    name={"treatments"}
                                    type={"checkbox"}
                                    value={treatment}
                                  />
                                )
                              )}
                            </Col>
                          ) : undefined}
                          <Col lg={30} md={30} sm={30}>
                            <p className={"mb1 mt1"}>
                              <span className={"fw8"}>
                                {t("group.findings.report.reattack.title")}
                              </span>
                            </p>
                            {_.isEmpty(values.closingDate) ? (
                              <React.Fragment>
                                {["REQUESTED", "ON_HOLD", "VERIFIED"].map(
                                  (verification): JSX.Element => (
                                    <Field
                                      component={FormikCheckbox}
                                      key={verification}
                                      label={t(
                                        `group.findings.report.reattack.${verification.toLowerCase()}`
                                      )}
                                      name={"verifications"}
                                      type={"checkbox"}
                                      value={verification}
                                    />
                                  )
                                )}
                              </React.Fragment>
                            ) : (
                              <React.Fragment>
                                {["VERIFIED"].map(
                                  (verification): JSX.Element => (
                                    <Field
                                      component={FormikCheckbox}
                                      key={verification}
                                      label={t(
                                        `group.findings.report.reattack.${verification.toLowerCase()}`
                                      )}
                                      name={"verifications"}
                                      type={"checkbox"}
                                      value={verification}
                                    />
                                  )
                                )}
                              </React.Fragment>
                            )}
                          </Col>
                          <Col lg={20} md={20} sm={20}>
                            <p className={"mb1 mt1"}>
                              <span className={"fw8"}>
                                {t("group.findings.report.state")}
                              </span>
                            </p>
                            {_.isEmpty(values.closingDate) ? (
                              <React.Fragment>
                                {["CLOSED", "OPEN"].map(
                                  (state): JSX.Element => (
                                    <Field
                                      component={FormikCheckbox}
                                      key={state}
                                      label={t(
                                        `searchFindings.tabVuln.${state.toLowerCase()}`
                                      )}
                                      name={"states"}
                                      type={"checkbox"}
                                      value={state}
                                    />
                                  )
                                )}
                              </React.Fragment>
                            ) : (
                              <React.Fragment>
                                {["CLOSED"].map(
                                  (state): JSX.Element => (
                                    <Field
                                      component={FormikCheckbox}
                                      key={state}
                                      label={t(
                                        `searchFindings.tabVuln.${state.toLowerCase()}`
                                      )}
                                      name={"states"}
                                      type={"checkbox"}
                                      value={state}
                                    />
                                  )
                                )}
                              </React.Fragment>
                            )}
                          </Col>
                        </Row>
                        <Hr />
                        <Button
                          id={"report-excel"}
                          type={"submit"}
                          variant={"primary"}
                        >
                          <FontAwesomeIcon icon={faFileExcel} />
                          &nbsp;{t("group.findings.report.generateXls")}
                        </Button>
                      </Form>
                    );
                  }}
                </Formik>
              );
            }}
          </VerifyDialog>
        </Col100>
      </Modal>
    </React.StrictMode>
  );
};

export { FilterReportModal };
