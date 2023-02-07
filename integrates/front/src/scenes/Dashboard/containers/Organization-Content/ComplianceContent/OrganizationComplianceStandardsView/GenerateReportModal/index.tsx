import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileContract } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IGenerateReportModalProps, ITableRowData } from "./types";

import { GET_UNFULFILLED_STANDARD_REPORT_URL } from "../queries";
import type { IUnfulfilledStandardAttr } from "../types";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { Tooltip } from "components/Tooltip";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import type { IVerifyFn } from "scenes/Dashboard/components/VerifyDialog/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";

const GenerateReportModal: React.FC<IGenerateReportModalProps> = ({
  isOpen,
  onClose,
  groupName,
  unfulfilledStandards,
}: IGenerateReportModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);
  const [disableVerify, setDisableVerify] = useState(false);
  const tableData = unfulfilledStandards.map(
    (unfulfilledStandard: IUnfulfilledStandardAttr): ITableRowData => ({
      ...unfulfilledStandard,
      include: true,
    })
  );

  const handleClose = useCallback((): void => {
    onClose();
    setIsVerifyDialogOpen(false);
  }, [onClose, setIsVerifyDialogOpen]);

  const [requestUnfulfilledStandardReport] = useLazyQuery<{
    unfulfilledStandardReportUrl: string;
  }>(GET_UNFULFILLED_STANDARD_REPORT_URL, {
    onCompleted: (data): void => {
      setDisableVerify(false);
      openUrl(data.unfulfilledStandardReportUrl);
      msgSuccess(
        t("organization.tabs.compliance.tabs.standards.alerts.generatedReport"),
        t("groupAlerts.titleSuccess")
      );
      setIsVerifyDialogOpen(false);
      onClose();
    },
    onError: (errors: ApolloError): void => {
      setDisableVerify(false);
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
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

  const handleRequestUnfulfilledStandardReport = useCallback(
    (verificationCode: string): void => {
      setDisableVerify(true);
      requestUnfulfilledStandardReport({
        variables: {
          groupName,
          verificationCode,
        },
      });
      mixpanel.track("UnfulfilledStandardReportRequest");
    },
    [requestUnfulfilledStandardReport, groupName]
  );

  const onRequestReport = useCallback(
    (setVerifyCallbacks: IVerifyFn): (() => void) =>
      (): void => {
        setVerifyCallbacks(
          (verificationCode: string): void => {
            handleRequestUnfulfilledStandardReport(verificationCode);
          },
          (): void => {
            setIsVerifyDialogOpen(false);
          }
        );
        setIsVerifyDialogOpen(true);
      },
    [handleRequestUnfulfilledStandardReport]
  );

  const columns: ColumnDef<ITableRowData>[] = [
    {
      accessorKey: "title",
      header: "Unfulfilled standard",
    },
  ];

  return (
    <React.StrictMode>
      <Modal
        minWidth={550}
        onClose={handleClose}
        open={isOpen}
        title={t(
          "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
        )}
      >
        <VerifyDialog disable={disableVerify} isOpen={isVerifyDialogOpen}>
          {(setVerifyCallbacks): JSX.Element => {
            return (
              <Fragment>
                <Table
                  columns={columns}
                  data={tableData}
                  id={"standardsToGenerateReport"}
                />
                <br />

                <Tooltip
                  id={
                    "organization.tabs.compliance.tabs.standards.buttons.generateReport.tooltip"
                  }
                  tip={t(
                    "organization.tabs.compliance.tabs.standards.buttons.generateReport.tooltip"
                  )}
                >
                  <Button
                    id={"standard-report"}
                    onClick={onRequestReport(setVerifyCallbacks)}
                    variant={"secondary"}
                  >
                    <FontAwesomeIcon icon={faFileContract} />
                    &nbsp;
                    {t(
                      "organization.tabs.compliance.tabs.standards.buttons.generateReport.text"
                    )}
                  </Button>
                </Tooltip>
              </Fragment>
            );
          }}
        </VerifyDialog>
      </Modal>
    </React.StrictMode>
  );
};

export { GenerateReportModal };
