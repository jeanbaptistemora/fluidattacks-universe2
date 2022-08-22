import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel } from "@fortawesome/free-solid-svg-icons";
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
import { array, object } from "yup";

import { Button } from "components/Button";
import { Col, Hr, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Tooltip } from "components/Tooltip";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { Col100 } from "styles/styledComponents";
import { FormikCheckbox, FormikDate, FormikDropdown } from "utils/forms/fields";
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
  closingDate: string;
  findingTitle: string;
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
      closingDate: string | undefined,
      findingTitle: string | undefined,
      states: string[],
      treatments: string[] | undefined,
      verifications: string[],
      verificationCode: string
    ): void => {
      const reportType = "XLS";
      mixpanel.track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          closingDate,
          findingTitle,
          groupName,
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
                closingDate: string;
                findingTitle: string;
                states: string[];
                treatments: string[];
                verifications: string[];
              }): void {
                setVerifyCallbacks(
                  (verificationCode: string): void => {
                    handleRequestGroupReport(
                      _.isEmpty(values.closingDate)
                        ? undefined
                        : values.closingDate,
                      _.isEmpty(values.findingTitle)
                        ? undefined
                        : values.findingTitle,
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
                    closingDate: "",
                    findingTitle: "",
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
                          <Col lg={50} md={90} sm={90}>
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
