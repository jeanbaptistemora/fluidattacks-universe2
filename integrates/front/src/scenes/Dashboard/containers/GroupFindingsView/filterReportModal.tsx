import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { array, object } from "yup";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ButtonToolbar, Col100, RequiredField } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IDeactivationModalProps {
  isOpen: boolean;
  onClose: () => void;
  closeReportsModal: () => void;
}

const FilterReportModal: React.FC<IDeactivationModalProps> = ({
  isOpen,
  onClose,
  closeReportsModal,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

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
      states: string[],
      treatments: string[],
      verifications: string[],
      verificationCode: string
    ): void => {
      const reportType = "XLS";
      mixpanel.track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
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
    treatments: array().min(1, t("validations.someRequired")),
  });

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={t("group.findings.report.modalTitle")}
      >
        <Col100>
          <VerifyDialog isOpen={isVerifyDialogOpen}>
            {(setVerifyCallbacks): JSX.Element => {
              function onRequestReport(values: {
                states: string[];
                treatments: string[];
                verifications: string[];
              }): void {
                setVerifyCallbacks(
                  (verificationCode: string): void => {
                    handleRequestGroupReport(
                      values.states,
                      values.treatments,
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
                    states: [],
                    treatments: [],
                    verifications: [],
                  }}
                  name={"reportTreatments"}
                  onSubmit={onRequestReport}
                  validationSchema={validations}
                >
                  <Form>
                    <p className={"mb0"}>
                      {t("group.findings.report.filterReportDescription")}
                    </p>
                    <Row align={"flex-start"} justify={"space-between"}>
                      <Col large={"50"} medium={"50"} small={"50"}>
                        <p>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
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
                      <Col large={"30"} medium={"30"} small={"30"}>
                        <p>
                          <span className={"fw8"}>
                            {t("group.findings.report.reattack.title")}
                          </span>
                        </p>
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
                      </Col>
                      <Col large={"20"} medium={"20"} small={"20"}>
                        <p>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          <span className={"fw8"}>
                            {t("group.findings.report.state")}
                          </span>
                        </p>
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
                      </Col>
                    </Row>
                    <hr />
                    <Row>
                      <ButtonToolbar>
                        <Button
                          id={"report-excel"}
                          type={"submit"}
                          variant={"primary"}
                        >
                          <FontAwesomeIcon icon={faFileExcel} />
                          &nbsp;{t("group.findings.report.generateXls")}
                        </Button>
                      </ButtonToolbar>
                    </Row>
                  </Form>
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
