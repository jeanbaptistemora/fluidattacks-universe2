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
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { FilterReportModal } from "../filterReportModal";
import { setReportType } from "../helpers";
import { REQUEST_GROUP_REPORT } from "../queries";
import { Button, ButtonGroup } from "components/Button";
import { Gap } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import type { IVerifyFn } from "scenes/Dashboard/components/VerifyDialog/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IReportOptionsProps {
  enableCerts: boolean;
  isFilterReportModalOpen: boolean;
  setVerifyCallbacks: IVerifyFn;
  typesOptions: string[];
  userRole: string;
  onClose: () => void;
  closeFilterReportsModal: () => void;
  setIsVerifyDialogOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsFilterReportModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ReportOptions: React.FC<IReportOptionsProps> = ({
  closeFilterReportsModal,
  enableCerts,
  isFilterReportModalOpen,
  onClose,
  setIsFilterReportModalOpen,
  setIsVerifyDialogOpen,
  setVerifyCallbacks,
  typesOptions,
  userRole,
}: IReportOptionsProps): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const openFilterReportModal: () => void = useCallback((): void => {
    setIsFilterReportModalOpen(true);
  }, [setIsFilterReportModalOpen]);

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        t("groupAlerts.reportRequested"),
        t("groupAlerts.titleSuccess")
      );
      setIsVerifyDialogOpen(false);
      closeFilterReportsModal();
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

  const handleRequestGroupReport = useCallback(
    (reportType: string, verificationCode: string): void => {
      mixpanel.track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          groupName,
          reportType,
          verificationCode,
        },
      });
    },
    [groupName, requestGroupReport]
  );

  const onRequestReport = useCallback(
    (event: React.MouseEvent<HTMLElement>): void => {
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
    },
    [handleRequestGroupReport, setVerifyCallbacks, setIsVerifyDialogOpen]
  );

  return (
    <Gap>
      {userRole === "user_manager" ? (
        <Tooltip
          id={"group.findings.report.certTooltip.id"}
          tip={t("group.findings.report.certTooltip")}
        >
          <Button
            disabled={!enableCerts}
            id={"report-cert"}
            onClick={onRequestReport}
            variant={"secondary"}
          >
            <FontAwesomeIcon icon={faFileContract} />
            &nbsp;
            {t("group.findings.report.cert")}
          </Button>
        </Tooltip>
      ) : undefined}
      <Tooltip
        id={"group.findings.report.pdfTooltip.id"}
        tip={t("group.findings.report.pdfTooltip")}
      >
        <Button
          id={"report-pdf"}
          onClick={onRequestReport}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faFilePdf} />
          &nbsp;
          {t("group.findings.report.pdf")}
        </Button>
      </Tooltip>
      <ButtonGroup>
        <Button
          id={"report-excel"}
          onClick={onRequestReport}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faFileExcel} />
          &nbsp;
          {t("group.findings.report.xls")}
        </Button>
        <Button
          id={"customize-report"}
          onClick={openFilterReportModal}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faSlidersH} />
        </Button>
      </ButtonGroup>
      <Tooltip
        id={"group.findings.report.dataTooltip.id"}
        tip={t("group.findings.report.dataTooltip")}
      >
        <Button
          id={"report-zip"}
          onClick={onRequestReport}
          variant={"secondary"}
        >
          <FontAwesomeIcon icon={faFileArchive} />
          &nbsp;
          {t("group.findings.report.data")}
        </Button>
      </Tooltip>
      <FilterReportModal
        closeReportsModal={onClose}
        isOpen={isFilterReportModalOpen}
        onClose={closeFilterReportsModal}
        typesOptions={typesOptions}
      />
    </Gap>
  );
};
