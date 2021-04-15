import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import type { IHistoricTreatment } from "../../../containers/DescriptionView/types";
import { Button } from "components/Button";
import { statusFormatter } from "components/DataTableNext/formatters";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { PointStatus } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { ButtonToolbar } from "styles/styledComponents";

interface IAdditionalInfoProps {
  canDisplayAnalyst: boolean;
  vulnerability: IVulnRowAttr;
  onClose: () => void;
}

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap pb1",
})``;

const Col40: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr2 w-40-l w-100-m w-100-ns",
})``;

const Col60: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr2 w-60-l w-100-m w-100-ns",
})``;

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr2 pb2 w-100",
})``;

const Col50: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "w-50-l w-50-m w-100-ns",
})``;

const Field: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: "ma0 mid-gray w-fit-content ws-pre-wrap ww-break-word",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "black f5 lh-title fw5",
})``;

const StatusLabel: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "f4",
})``;

const Status: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "f2-5",
})``;

export const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canDisplayAnalyst,
  vulnerability,
  onClose,
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
      : "";

  const currentJustification: string =
    vulnerability.currentState === "closed" ||
    _.isUndefined(lastTreatment.justification) ||
    _.isEmpty(lastTreatment.justification)
      ? ""
      : lastTreatment.justification;

  return (
    <React.StrictMode>
      <Col100>
        <Col100>
          <Status>
            <b>
              <PointStatus status={vulnerability.currentStateCapitalized} />
            </b>
          </Status>
        </Col100>
        <Col100>
          <b>{t("searchFindings.tabVuln.vulnTable.location")}</b>
        </Col100>
        <Row>
          <Col40>
            <Label>{t("searchFindings.tabVuln.vulnTable.where")}</Label>
          </Col40>
          <Col100>
            <Field>{vulnerability.where}</Field>
            {_.isEmpty(vulnerability.stream) ? undefined : (
              <React.Fragment>
                <br />
                <Field>{vulnerability.stream}</Field>
              </React.Fragment>
            )}
          </Col100>
        </Row>
        <Row>
          <Col40>
            <Label>{t("searchFindings.tabVuln.vulnTable.specific")}</Label>
          </Col40>
          <Col100>
            <Field>{vulnerability.specific}</Field>
          </Col100>
        </Row>
        <Row>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.reattacks")}</b>
            </Col100>
            <Row>
              <Col40>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.lastRequestedReattackDate"
                  )}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.lastRequestedReattackDate} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>{t("searchFindings.tabVuln.vulnTable.requester")}</Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.lastReattackRequester} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>{t("searchFindings.tabVuln.vulnTable.cycles")}</Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.cycles} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>{t("searchFindings.tabVuln.vulnTable.efficacy")}</Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.efficacy} />
              </Col60>
            </Row>
          </Col50>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.treatments")}</b>
            </Col100>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.currentTreatment")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.treatment} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentManager")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.treatmentManager} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentDate")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.treatmentDate} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentExpiration")}
                </Label>
              </Col40>
              <Col60>
                <Value value={currentExpiration} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentJustification")}
                </Label>
              </Col40>
              <Col60>
                <Value value={currentJustification} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentChanges")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.treatmentChanges} />
              </Col60>
            </Row>
          </Col50>
        </Row>
        <Row>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.info")}</b>
            </Col100>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.reportDate")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.reportDate} />
              </Col60>
            </Row>
            {_.isEmpty(vulnerability.commitHash) ? undefined : (
              <Row>
                <Col40>
                  <Label>{t("searchFindings.tabVuln.commitHash")}</Label>
                </Col40>
                <Col60>
                  <p
                    className={
                      "ma0 mid-gray pr2-l tr-l tl-m tl-ns w-fit-content ws-pre-wrap ww-break-word"
                    }
                  >
                    {vulnerability.commitHash}
                  </p>
                </Col60>
              </Row>
            )}
            <Row>
              <Col40>
                <Label>{t("searchFindings.tabDescription.tag")}</Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.tag} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabDescription.businessCriticality")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.severity} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.vulnType.title")}
                </Label>
              </Col40>
              <Col60>
                <Value value={vulnerability.vulnType} />
              </Col60>
            </Row>
            <Row>
              <Col40>
                <Label>{t("searchFindings.tabDescription.zeroRisk")}</Label>
              </Col40>
              <Col60>
                {_.isEmpty(vulnerability.zeroRisk) ? (
                  <Value value={vulnerability.zeroRisk} />
                ) : (
                  <StatusLabel>
                    {statusFormatter(vulnerability.zeroRisk)}
                  </StatusLabel>
                )}
              </Col60>
            </Row>
            {canDisplayAnalyst ? (
              <Row>
                <Col40>
                  <Label>{t("searchFindings.tabDescription.analyst")}</Label>
                </Col40>
                <Col60>
                  <Value value={vulnerability.analyst} />
                </Col60>
              </Row>
            ) : undefined}
          </Col50>
        </Row>
      </Col100>
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button id={"close-vuln-modal"} onClick={onClose}>
              {t("searchFindings.tabVuln.close")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </Row>
    </React.StrictMode>
  );
};
