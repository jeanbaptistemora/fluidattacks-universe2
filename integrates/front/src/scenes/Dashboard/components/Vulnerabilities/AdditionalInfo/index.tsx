import type { IHistoricTreatment } from "../../../containers/DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import React from "react";
import type { StyledComponent } from "styled-components";
import _ from "lodash";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { statusFormatter } from "components/DataTableNext/formatters";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import {
  Col100,
  Col40,
  Col60,
  EditableFieldNotUrl,
  Row,
} from "styles/styledComponents";

interface IAdditionalInfoProps {
  canDisplayAnalyst: boolean;
  vulnerability: IVulnRowAttr;
}

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "f4",
})``;

export const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canDisplayAnalyst,
  vulnerability,
}: IAdditionalInfoProps): JSX.Element => {
  const { t } = useTranslation();

  const lastTreatment: IHistoricTreatment = getLastTreatment(
    vulnerability.historicTreatment
  );
  const currentExpiration: string =
    vulnerability.currentState === "open" &&
    lastTreatment.treatment === "ACCEPTED" &&
    !_.isUndefined(lastTreatment.acceptanceDate)
      ? lastTreatment.acceptanceDate
      : "-";

  return (
    <React.StrictMode>
      <Col100>
        <ul>
          <li>
            <b>{t("search_findings.tab_vuln.vulnTable.location")}</b>
            <ul>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_vuln.vulnTable.where")}</b>
                  </Col40>
                  <Col100>
                    <EditableFieldNotUrl>
                      {vulnerability.where}
                    </EditableFieldNotUrl>
                  </Col100>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_vuln.vulnTable.specific")}</b>
                  </Col40>
                  <Col60>{vulnerability.specific}</Col60>
                </Row>
              </li>
            </ul>
          </li>
          <li>
            <b>{t("search_findings.tab_vuln.vulnTable.reattacks")}</b>
            <ul>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t(
                        "search_findings.tab_vuln.vulnTable.lastRequestedReattackDate"
                      )}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.lastRequestedReattackDate}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_vuln.vulnTable.requester")}</b>
                  </Col40>
                  <Col60>{vulnerability.lastReattackRequester}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_vuln.vulnTable.cycles")}</b>
                  </Col40>
                  <Col60>{vulnerability.cycles}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_vuln.vulnTable.efficacy")}</b>
                  </Col40>
                  <Col60>{vulnerability.efficacy}</Col60>
                </Row>
              </li>
            </ul>
          </li>
          <li>
            <b>{t("search_findings.tab_vuln.vulnTable.treatments")}</b>
            <ul>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t("search_findings.tab_description.treatment.title")}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.treatment}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_description.treatment_mgr")}</b>
                  </Col40>
                  <Col60>{vulnerability.treatmentManager}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t("search_findings.tab_vuln.vulnTable.treatmentDate")}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.treatmentDate}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t(
                        "search_findings.tab_vuln.vulnTable.treatmentExpiration"
                      )}
                    </b>
                  </Col40>
                  <Col60>{currentExpiration}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t("search_findings.tab_vuln.vulnTable.treatmentChanges")}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.treatmentChanges}</Col60>
                </Row>
              </li>
            </ul>
          </li>
          <li>
            <b>{t("search_findings.tab_vuln.vulnTable.info")}</b>
            <ul>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_description.tag")}</b>
                  </Col40>
                  <Col60>{vulnerability.tag}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t(
                        "search_findings.tab_description.business_criticality"
                      )}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.severity}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>
                      {t("search_findings.tab_vuln.vulnTable.vulnType.title")}
                    </b>
                  </Col40>
                  <Col60>{vulnerability.vulnType}</Col60>
                </Row>
              </li>
              <li>
                <Row>
                  <Col40>
                    <b>{t("search_findings.tab_description.zero_risk")}</b>
                  </Col40>
                  <Col60>
                    <Label>{statusFormatter(vulnerability.zeroRisk)}</Label>
                  </Col60>
                </Row>
              </li>
              {canDisplayAnalyst ? (
                <li>
                  <Row>
                    <Col40>
                      <b>{t("search_findings.tab_description.analyst")}</b>
                    </Col40>
                    <Col60>{vulnerability.analyst}</Col60>
                  </Row>
                </li>
              ) : undefined}
            </ul>
          </li>
        </ul>
      </Col100>
    </React.StrictMode>
  );
};
