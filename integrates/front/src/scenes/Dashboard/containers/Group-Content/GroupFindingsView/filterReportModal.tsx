import type { ApolloError } from "@apollo/client";
import { useLazyQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { FilterForm } from "./filterForm";
import { REQUEST_GROUP_REPORT } from "./queries";

import { Col } from "components/Layout";
import { Modal } from "components/Modal";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IDeactivationModalProps {
  isOpen: boolean;
  onClose: () => void;
  typesOptions: string[];
  closeReportsModal: () => void;
}

const FilterReportModal: React.FC<IDeactivationModalProps> = ({
  isOpen,
  onClose,
  typesOptions,
  closeReportsModal,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const handleClose = useCallback((): void => {
    onClose();
    setIsVerifyDialogOpen(false);
  }, [onClose, setIsVerifyDialogOpen]);

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      handleClose();
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
      lastReport: number | undefined,
      location: string | undefined,
      maxReleaseDate: string | undefined,
      maxSeverity: number | undefined,
      minReleaseDate: string | undefined,
      minSeverity: number | undefined,
      states: string[],
      treatments: string[] | undefined,
      verifications: string[],
      verificationCode: string
      // Exception: FP(parameters are necessary)
      // eslint-disable-next-line
    ): void => { // NOSONAR
      const reportType = "XLS";
      mixpanel.track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          age,
          closingDate,
          findingTitle,
          groupName,
          lastReport,
          location,
          maxReleaseDate,
          maxSeverity,
          minReleaseDate,
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

  return (
    <React.StrictMode>
      <Modal
        minWidth={600}
        onClose={handleClose}
        open={isOpen}
        title={t("group.findings.report.modalTitle")}
      >
        <Col>
          <VerifyDialog isOpen={isVerifyDialogOpen}>
            {(setVerifyCallbacks): JSX.Element => {
              return (
                <FilterForm
                  requestGroupReport={handleRequestGroupReport}
                  setIsVerifyDialogOpen={setIsVerifyDialogOpen}
                  setVerifyCallbacks={setVerifyCallbacks}
                  typesOptions={typesOptions}
                />
              );
            }}
          </VerifyDialog>
        </Col>
      </Modal>
    </React.StrictMode>
  );
};

export { FilterReportModal };
