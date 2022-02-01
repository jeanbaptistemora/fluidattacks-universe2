import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React from "react";
import { Trans } from "react-i18next";
import { useParams } from "react-router-dom";
import { array, object } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IDeactivationModalProps {
  hasMobileApp: boolean;
  isOpen: boolean;
  onClose: () => void;
}

const FilterReportModal: React.FC<IDeactivationModalProps> = ({
  hasMobileApp,
  isOpen,
  onClose,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        translate.t("groupAlerts.reportRequested"),
        translate.t("groupAlerts.titleSuccess")
      );
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - The user already has a requested report for the same group"
        ) {
          msgError(translate.t("groupAlerts.reportAlreadyRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred requesting group report", error);
        }
      });
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
    treatments: array().min(1, translate.t("validations.someRequired")),
  });

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("group.findings.report.modalTitle")}
        onEsc={onClose}
        open={isOpen}
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
                    <p>
                      {translate.t("group.findings.report.techDescription")}
                    </p>
                  </Trans>
                  <p>
                    {translate.t(
                      "group.findings.report.filterReportDescription"
                    )}
                  </p>
                  <p className={"tl fw8"}>
                    {translate.t("group.findings.report.treatment")}
                  </p>
                  {["NEW", "IN_PROGRESS", "ACCEPTED", "ACCEPTED_UNDEFINED"].map(
                    (treatment): JSX.Element => (
                      <Field
                        component={FormikCheckbox}
                        key={treatment}
                        label={translate.t(
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
                      <Button id={"report-excel"} type={"submit"}>
                        <FontAwesomeIcon icon={faFileExcel} />
                        {translate.t("group.findings.report.generateXls")}
                      </Button>
                    </ButtonToolbar>
                  </Row>
                </Form>
              </Formik>
            ) : (
              <React.Fragment>
                <p>{translate.t("group.findings.report.noMobileAppWarning")}</p>
                <p>
                  <a
                    href={
                      "https://apps.apple.com/us/app/integrates/id1470450298"
                    }
                    rel={"nofollow noopener noreferrer"}
                    target={"_blank"}
                  >
                    <img
                      alt={"App Store"}
                      height={"40"}
                      src={AppstoreBadge}
                      width={"140"}
                    />
                  </a>
                  <a
                    href={
                      "https://play.google.com/store/apps/details?id=com.fluidattacks.integrates"
                    }
                    rel={"nofollow noopener noreferrer"}
                    target={"_blank"}
                  >
                    <img
                      alt={"Google Play"}
                      height={"40"}
                      src={GoogleplayBadge}
                      width={"140"}
                    />
                  </a>
                </p>
              </React.Fragment>
            )}
          </Col100>
        </div>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClose}>
                {translate.t("group.findings.report.modalClose")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { FilterReportModal };
