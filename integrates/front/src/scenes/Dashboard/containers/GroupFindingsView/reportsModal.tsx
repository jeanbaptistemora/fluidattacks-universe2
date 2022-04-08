import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faFileArchive,
  faFileContract,
  faFileExcel,
  faFilePdf,
  faSlidersH,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { setReportType } from "./helpers";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import { FilterReportModal } from "scenes/Dashboard/containers/GroupFindingsView/filterReportModal";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ButtonToolbarCenter, Col100, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IDeactivationModalProps {
  filledGroupInfo: boolean;
  isOpen: boolean;
  onClose: () => void;
  userRole: string;
}

const ReportsModal: React.FC<IDeactivationModalProps> = ({
  filledGroupInfo,
  isOpen,
  onClose,
  userRole,
}: IDeactivationModalProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const [isFilterReportModalOpen, setFilterReportModalOpen] = useState(false);
  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const openFilterReportModal: () => void = useCallback((): void => {
    setFilterReportModalOpen(true);
  }, []);
  const closeFilterReportsModal: () => void = useCallback((): void => {
    setFilterReportModalOpen(false);
  }, []);

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        t("groupAlerts.reportRequested"),
        t("groupAlerts.titleSuccess")
      );
      setIsVerifyDialogOpen(false);
      onClose();
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

  function handleRequestGroupReport(
    reportType: string,
    verificationCode: string
  ): void {
    mixpanel.track("GroupReportRequest", { reportType });

    requestGroupReport({
      variables: {
        groupName,
        reportType,
        verificationCode,
      },
    });
  }

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
              function onRequestReport(
                event: React.MouseEvent<HTMLElement>
              ): void {
                const target: HTMLElement = event.currentTarget as HTMLElement;
                const icon: SVGElement | null = target.querySelector("svg");
                if (icon !== null) {
                  const reportType: string = setReportType(icon);
                  setVerifyCallbacks(
                    (verificationCode: string): void => {
                      handleRequestGroupReport(reportType, verificationCode);
                    },
                    (): void => {
                      setIsVerifyDialogOpen(false);
                    }
                  );
                  setIsVerifyDialogOpen(true);
                }
              }

              return (
                <Row>
                  <Col100>
                    <ButtonToolbarCenter>
                      <TooltipWrapper
                        id={"group.findings.report.certTooltip.id"}
                        message={t("group.findings.report.certTooltip")}
                      >
                        <Button
                          disabled={!filledGroupInfo}
                          hidden={userRole !== "user_manager"}
                          id={"report-cert"}
                          onClick={onRequestReport}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faFileContract} />
                          {t("group.findings.report.cert")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        id={"group.findings.report.pdfTooltip.id"}
                        message={t("group.findings.report.pdfTooltip")}
                      >
                        <Button
                          id={"report-pdf"}
                          onClick={onRequestReport}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faFilePdf} />
                          {t("group.findings.report.pdf")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        id={"group.findings.report.xlsTooltip.id"}
                        message={t("group.findings.report.xlsTooltip")}
                      >
                        <Button
                          id={"report-excel"}
                          onClick={onRequestReport}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faFileExcel} />
                          {t("group.findings.report.xls")}
                        </Button>
                        <Button
                          id={"customize-report"}
                          onClick={openFilterReportModal}
                          // eslint-disable-next-line react/forbid-component-props
                          style={{ borderLeft: "0", marginLeft: "0" }}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faSlidersH} />
                        </Button>
                        <FilterReportModal
                          closeReportsModal={onClose}
                          isOpen={isFilterReportModalOpen}
                          onClose={closeFilterReportsModal}
                        />
                      </TooltipWrapper>
                      <TooltipWrapper
                        id={"group.findings.report.dataTooltip.id"}
                        message={t("group.findings.report.dataTooltip")}
                      >
                        <Button
                          id={"report-zip"}
                          onClick={onRequestReport}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faFileArchive} />
                          {t("group.findings.report.data")}
                        </Button>
                      </TooltipWrapper>
                    </ButtonToolbarCenter>
                  </Col100>
                </Row>
              );
            }}
          </VerifyDialog>
        </Col100>
        <ModalFooter>
          <Button onClick={onClose} variant={"secondary"}>
            {t("group.findings.report.modalClose")}
          </Button>
        </ModalFooter>
      </Modal>
    </React.StrictMode>
  );
};

export { ReportsModal };
