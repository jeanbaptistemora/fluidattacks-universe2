import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faFileExcel } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { track } from "mixpanel-browser";
import React, { useState } from "react";
import { Trans } from "react-i18next";
import { useParams } from "react-router-dom";

import { setReportType } from "./helpers";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { REQUEST_GROUP_REPORT } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ButtonToolbar, Col100, Row, Select } from "styles/styledComponents";
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

  const [selectedTreatment, setSelectedTreatment] = useState("");
  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setSelectedTreatment(event.target.value);
  }

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
      const treatment: string = selectedTreatment;

      track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          groupName,
          reportType,
          treatment,
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
                <Trans>
                  <p>
                    {translate.t(
                      "group.findings.report.filterReportDescription"
                    )}
                  </p>
                </Trans>
                <Row />
                <Trans>
                  <p className={"tl fw8"}>
                    {translate.t("group.findings.report.treatment")}
                  </p>
                </Trans>
                <Select onChange={onTreatmentChange}>
                  <option disabled={true} selected={true} value={""}>
                    {"Select one"}
                  </option>
                  <option value={"IN_PROGRESS"}>
                    {translate.t(
                      "searchFindings.tabDescription.treatment.inProgress"
                    )}
                  </option>
                  <option value={"ACCEPTED"}>
                    {translate.t(
                      "searchFindings.tabDescription.treatment.accepted"
                    )}
                  </option>
                  <option value={"ACCEPTED_UNDEFINED"}>
                    {translate.t(
                      "searchFindings.tabDescription.treatment.acceptedUndefined"
                    )}
                  </option>
                </Select>
                <br />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button
                        id={"report-excel"}
                        onClick={handleRequestGroupReport}
                      >
                        <FontAwesomeIcon icon={faFileExcel} />
                        {translate.t("group.findings.report.generateXls")}
                      </Button>
                    </ButtonToolbar>
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

export { FilterReportModal };
