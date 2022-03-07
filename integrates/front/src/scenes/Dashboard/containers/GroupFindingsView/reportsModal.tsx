import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faFileArchive,
  faFileExcel,
  faFilePdf,
  faSlidersH,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { Trans } from "react-i18next";
import { useParams } from "react-router-dom";

import { setReportType } from "./helpers";

import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { FilterReportModal } from "scenes/Dashboard/containers/GroupFindingsView/filterReportModal";
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

const DOCS_URL = "https://docs.fluidattacks.com/machine/web/groups/reports";

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

  const [isFilterReportModalOpen, setFilterReportModalOpen] = useState(false);
  const openFilterReportModal: () => void = useCallback((): void => {
    setFilterReportModalOpen(true);
  }, []);
  const closeFilterReportsModal: () => void = useCallback((): void => {
    setFilterReportModalOpen(false);
  }, []);

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
        onClose={onClose}
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
                          variant={"secondary"}
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
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faFileExcel} />
                          {translate.t("group.findings.report.xls")}
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
                          hasMobileApp={hasMobileApp}
                          isOpen={isFilterReportModalOpen}
                          onClose={closeFilterReportsModal}
                        />
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
                          variant={"secondary"}
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
            <p>
              {translate.t("group.findings.report.passphraseOptOut")}&nbsp;
              <ExternalLink href={`${DOCS_URL}#remove-passphrase`}>
                {`${DOCS_URL}#remove-passphrase`}
              </ExternalLink>
            </p>
          </Col100>
        </div>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClose} variant={"secondary"}>
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
