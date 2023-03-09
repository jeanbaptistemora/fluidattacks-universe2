import type { ApolloError } from "@apollo/client";
import { useLazyQuery } from "@apollo/client";
import { faFileExport } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import type { FormEvent } from "react";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { Text } from "components/Text";
import { VerifyDialog } from "scenes/Dashboard/components/VerifyDialog";
import type { IVerifyFn } from "scenes/Dashboard/components/VerifyDialog/types";
import { REQUEST_GROUP_TOE_LINES } from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeLinesView/ActionButtons/ExportButton/queries";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const ExportButton: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();

  const [isVerifyDialogOpen, setIsVerifyDialogOpen] = useState(false);

  const handleClose = useCallback((): void => {
    setIsVerifyDialogOpen(false);
  }, [setIsVerifyDialogOpen]);

  const [requestGroupToeLines] = useLazyQuery(REQUEST_GROUP_TOE_LINES, {
    onCompleted: (): void => {
      handleClose();
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
            Logger.warning(
              "An error occurred requesting toe lines report",
              error
            );
        }
      });
    },
  });
  const onRequestReport = useCallback(
    (
      setVerifyCallbacks: IVerifyFn
    ): ((event: FormEvent<HTMLButtonElement>) => void) => {
      return (event: FormEvent<HTMLButtonElement>): void => {
        event.stopPropagation();
        setVerifyCallbacks(
          (verificationCode: string): void => {
            requestGroupToeLines({
              variables: { groupName, verificationCode },
            });
          },
          (): void => {
            setIsVerifyDialogOpen(false);
          }
        );
        setIsVerifyDialogOpen(true);
      };
    },
    [groupName, requestGroupToeLines, setIsVerifyDialogOpen]
  );

  return (
    <React.StrictMode>
      <Can do={"api_resolvers_query_toe_lines_report_resolve"}>
        <VerifyDialog isOpen={isVerifyDialogOpen}>
          {(setVerifyCallbacks: IVerifyFn): JSX.Element => {
            return (
              <Button
                onClick={onRequestReport(setVerifyCallbacks)}
                variant={"ghost"}
              >
                <Text bright={3}>
                  <FontAwesomeIcon icon={faFileExport} />
                  &nbsp;
                  {t("group.findings.exportCsv.text")}
                </Text>
              </Button>
            );
          }}
        </VerifyDialog>
      </Can>
    </React.StrictMode>
  );
};

export { ExportButton };
