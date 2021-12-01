import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import type { IHistoricTreatment } from "../../../containers/DescriptionView/types";
import { Button } from "components/Button";
import { commitFormatter } from "components/DataTableNext/formatters";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { PointStatus } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { ButtonToolbar } from "styles/styledComponents";

interface IAdditionalInfoProps {
  canDisplayHacker: boolean;
  vulnerability: IVulnRowAttr;
  onClose: () => void;
}

const OuterRow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap pb1",
})``;

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-wrap-m pb1",
})``;

const LabelField: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 w-30-l w-100-m w-100-ns w-auto",
})``;

const InfoField: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 w-70-l w-100-m w-100-ns w-auto",
})``;

const Col100: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "pl1 pr0 pb1 w-100",
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
  className: "lh-title ma0 mid-gray w-fit-content ws-pre-wrap ww-break-word",
})``;

const Label: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "black f5 lh-title fw5",
})``;

const Status: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: "f2-5",
})``;

const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canDisplayHacker,
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
      <div className={"pb1 pt2 w-100"}>
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
        <div className={"flex flex-wrap pb0"}>
          <div className={"pl1 pr0 pb0 w-100"}>
            <Field>{vulnerability.where}</Field>
            {_.isEmpty(vulnerability.stream) ? undefined : (
              <Field>{vulnerability.stream}</Field>
            )}
          </div>
        </div>
        <OuterRow>
          <div className={"pl1 pr0 w-10-l w-100-m w-100-ns"}>
            <Label>
              {t(
                `searchFindings.tabVuln.vulnTable.specificType.${vulnerability.vulnerabilityType}`
              )}
            </Label>
          </div>
          <div className={"pl1 pr0 w-90-l w-100-m w-100-ns"}>
            <Field>{vulnerability.specific}</Field>
          </div>
        </OuterRow>
        <OuterRow>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.reattacks")}</b>
            </Col100>
            <Row>
              <LabelField>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.lastRequestedReattackDate"
                  )}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.lastRequestedReattackDate} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.requester")}</Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.lastReattackRequester} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.cycles")}</Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.cycles} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.efficacy")}</Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.efficacy} />
              </InfoField>
            </Row>
          </Col50>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.treatments")}</b>
            </Col100>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.currentTreatment")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.treatment} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentManager")}
                </Label>
              </LabelField>
              <InfoField>
                <p
                  className={
                    "f5 lh-title ma0 mid-gray pr1-l tr-l tl-m tl-ns truncate"
                  }
                >
                  {_.isEmpty(vulnerability.treatmentManager)
                    ? t("searchFindings.tabVuln.notApplicable")
                    : vulnerability.treatmentManager}
                </p>
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentDate")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.treatmentDate} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentExpiration")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={currentExpiration} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentJustification")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={currentJustification} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentChanges")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.treatmentChanges} />
              </InfoField>
            </Row>
          </Col50>
        </OuterRow>
        <OuterRow>
          <Col100>
            <b>{t("searchFindings.tabVuln.vulnTable.info")}</b>
          </Col100>
          <Col50>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.reportDate")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.reportDate} />
              </InfoField>
            </Row>
            {_.isEmpty(vulnerability.commitHash) ? undefined : (
              <Row>
                <LabelField>
                  <Label>{t("searchFindings.tabVuln.commitHash")}</Label>
                </LabelField>
                <InfoField>
                  <p
                    className={
                      "lh-title ma0 mid-gray pr1-l tr-l tl-m tl-ns ws-pre-wrap ww-break-word"
                    }
                  >
                    {commitFormatter(vulnerability.commitHash)}
                  </p>
                </InfoField>
              </Row>
            )}
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabDescription.tag")}</Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.tag} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabDescription.businessCriticality")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.severity} />
              </InfoField>
            </Row>
          </Col50>
          <Col50>
            <Row>
              <LabelField>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.vulnerabilityType.title"
                  )}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.vulnerabilityType} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabDescription.zeroRisk")}</Label>
              </LabelField>
              <div className={"pl1 pr0 w-70-l w-100-m w-100-ns mr"}>
                {_.isEmpty(vulnerability.zeroRisk) ? (
                  <Value value={vulnerability.zeroRisk} />
                ) : (
                  <div className={"tr-l tl-m tl-ns"}>
                    <p className={"dib f5 ma0 mid-gray pr1-l"}>
                      <PointStatus status={vulnerability.zeroRisk} />
                    </p>
                  </div>
                )}
              </div>
            </Row>
            {canDisplayHacker ? (
              <Row>
                <LabelField>
                  <Label>{t("searchFindings.tabDescription.hacker")}</Label>
                </LabelField>
                <InfoField>
                  <Value value={vulnerability.hacker} />
                </InfoField>
              </Row>
            ) : undefined}
          </Col50>
        </OuterRow>
      </div>
      <hr />
      <OuterRow>
        <Col100>
          <ButtonToolbar>
            <Button id={"close-vuln-modal"} onClick={onClose}>
              {t("searchFindings.tabVuln.close")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </OuterRow>
    </React.StrictMode>
  );
};

export { AdditionalInfo, Label };
