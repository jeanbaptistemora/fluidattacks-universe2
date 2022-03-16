import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { array, object } from "yup";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Modal, ModalFooter } from "components/Modal";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IDeactivationModalProps {
  hasMobileApp: boolean;
  isOpen: boolean;
  onClose: () => void;
  closeReportsModal: () => void;
}

const FilterReportModal: React.FC<IDeactivationModalProps> = ({
  hasMobileApp,
  isOpen,
  onClose,
  closeReportsModal,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      closeReportsModal();
      msgSuccess(
        t("groupAlerts.reportRequested"),
        t("groupAlerts.titleSuccess")
      );
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - The user already has a requested report for the same group"
        ) {
          msgError(t("groupAlerts.reportAlreadyRequested"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred requesting group report", error);
        }
      });
      closeReportsModal();
    },
  });

  function handleRequestGroupReport(values: { treatments: string[] }): void {
    const reportType = "XLS";
    track("GroupReportRequest", { reportType });

    requestGroupReport({
      variables: {
        groupName,
        reportType,
        treatments: values.treatments,
      },
    });
    onClose();
  }

  const validations = object().shape({
    treatments: array().min(1, t("validations.someRequired")),
  });

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={isOpen}
        title={t("group.findings.report.modalTitle")}
      >
        <div className={"flex flex-wrap"}>
          <Col100>
            {hasMobileApp ? (
              <Formik
                initialValues={{ treatments: [] }}
                name={"reportTreatments"}
                onSubmit={handleRequestGroupReport}
                validationSchema={validations}
              >
                <Form>
                  <Trans>
                    <p>{t("group.findings.report.techDescription")}</p>
                  </Trans>
                  <p>{t("group.findings.report.filterReportDescription")}</p>
                  <p className={"tl fw8"}>
                    {t("group.findings.report.treatment")}
                  </p>
                  {["NEW", "IN_PROGRESS", "ACCEPTED", "ACCEPTED_UNDEFINED"].map(
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
            ) : (
              <React.Fragment>
                <p>{t("group.findings.report.noMobileAppWarning")}</p>
                <p>
                  <ExternalLink
                    href={
                      "https://apps.apple.com/us/app/integrates/id1470450298"
                    }
                  >
                    <img
                      alt={"App Store"}
                      height={"40"}
                      src={AppstoreBadge}
                      width={"140"}
                    />
                  </ExternalLink>
                  <ExternalLink
                    href={
                      "https://play.google.com/store/apps/details?id=com.fluidattacks.integrates"
                    }
                  >
                    <img
                      alt={"Google Play"}
                      height={"40"}
                      src={GoogleplayBadge}
                      width={"140"}
                    />
                  </ExternalLink>
                </p>
              </React.Fragment>
            )}
          </Col100>
        </div>
        <div>
          <div>
            <ModalFooter>
              <Button onClick={onClose} variant={"secondary"}>
                {t("group.findings.report.modalClose")}
              </Button>
            </ModalFooter>
          </div>
        </div>
      </Modal>
    </React.StrictMode>
  );
};

export { FilterReportModal };
