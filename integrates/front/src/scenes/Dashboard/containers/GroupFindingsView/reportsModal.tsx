import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faFileArchive,
  faFileExcel,
  faFilePdf,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { track } from "mixpanel-browser";
import React from "react";
import { Trans } from "react-i18next";
import { useParams } from "react-router-dom";

import { setReportType } from "./helpers";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Row,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IDeactivationModalProps {
  hasMobileApp: boolean;
  isOpen: boolean;
  onClose: () => void;
}

const ReportsModal: React.FC<IDeactivationModalProps> = ({
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
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred requesting group report", error);
    },
  });

  function handleRequestGroupReport(
    event: React.MouseEvent<HTMLElement>
  ): void {
    const target: HTMLElement = event.currentTarget as HTMLElement;
    const icon: SVGElement | null = target.querySelector("svg");
    if (icon !== null) {
      const reportType: string = setReportType(icon);

      track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          groupName,
          reportType,
        },
      });
      onClose();
    }
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("group.findings.report.modalTitle")}
        onEsc={onClose}
        open={isOpen}
      >
        <div className={"flex flex-wrap tc"}>
          <Col100>
            {hasMobileApp ? (
              <React.Fragment>
                <Trans>
                  <p>{translate.t("group.findings.report.techDescription")}</p>
                </Trans>
                <br />
                <Row>
                  <Col100>
                    <ButtonToolbarCenter>
                      <TooltipWrapper
                        id={"group.findings.report.pdfTooltip.id"}
                        message={translate.t(
                          "group.findings.report.pdfTooltip"
                        )}
                      >
                        <Button
                          id={"report-pdf"}
                          onClick={handleRequestGroupReport}
                        >
                          <FontAwesomeIcon icon={faFilePdf} />
                          {translate.t("group.findings.report.pdf")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        id={"group.findings.report.xlsTooltip.id"}
                        message={translate.t(
                          "group.findings.report.xlsTooltip"
                        )}
                      >
                        <Button
                          id={"report-excel"}
                          onClick={handleRequestGroupReport}
                        >
                          <FontAwesomeIcon icon={faFileExcel} />
                          {translate.t("group.findings.report.xls")}
                        </Button>
                      </TooltipWrapper>
                      <TooltipWrapper
                        id={"group.findings.report.dataTooltip.id"}
                        message={translate.t(
                          "group.findings.report.dataTooltip"
                        )}
                      >
                        <Button
                          id={"report-zip"}
                          onClick={handleRequestGroupReport}
                        >
                          <FontAwesomeIcon icon={faFileArchive} />
                          {translate.t("group.findings.report.data")}
                        </Button>
                      </TooltipWrapper>
                    </ButtonToolbarCenter>
                  </Col100>
                </Row>
              </React.Fragment>
            ) : (
              <React.Fragment>
                <Trans>
                  <p>
                    {translate.t("group.findings.report.noMobileAppWarning")}
                  </p>
                </Trans>
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

export { ReportsModal };
