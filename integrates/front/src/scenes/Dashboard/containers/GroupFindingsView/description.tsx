import React from "react";
import { useTranslation } from "react-i18next";

import type { IVerificationSummaryAttr } from "./types";

import { Col33, Row } from "styles/styledComponents";

interface IDescriptionProps {
  description: string;
  isExploitable: boolean;
  lastVulnerability: number;
  openAge: number;
  state: string;
  treatment: string;
  verificationSummary: IVerificationSummaryAttr;
}

const Description = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  state,
  treatment,
  verificationSummary,
}: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const [treatmentNew, inProgress, temporallyAccepted, permanentlyAccepted] =
    treatment.split(",").map((line): string => line.trim());
  const isOpen = state === "open";

  return (
    <div>
      <h3>{t("group.findings.description.title")}</h3>
      <Row>
        <p>{description}</p>
      </Row>
      <Row>
        <Col33>
          {t("group.findings.description.lastReport")}&nbsp;
          {t("group.findings.description.value", { count: lastVulnerability })}
        </Col33>
        <Col33>{treatmentNew}</Col33>
        {isOpen ? (
          <Col33>
            {t("group.findings.description.onHold")}&nbsp;
            {verificationSummary.onHold}
          </Col33>
        ) : (
          <Col33 />
        )}
      </Row>
      <hr />
      <Row>
        <Col33>
          {t("group.findings.description.firstSeen")}&nbsp;
          {t("group.findings.description.value", { count: openAge })}
        </Col33>
        <Col33>{inProgress}</Col33>
        {isOpen ? (
          <Col33>
            {t("group.findings.description.requested")}&nbsp;
            {verificationSummary.requested}
          </Col33>
        ) : (
          <Col33 />
        )}
      </Row>
      <hr />
      <Row>
        <Col33>
          {t("group.findings.description.exploitable")}&nbsp;
          {t(
            isExploitable
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col33>
        <Col33>{temporallyAccepted}</Col33>
        {isOpen ? (
          <Col33>
            {t("group.findings.description.verified")}&nbsp;
            {verificationSummary.verified}
          </Col33>
        ) : (
          <Col33 />
        )}
      </Row>
      <hr />
      <Row>
        <Col33>
          {t("group.findings.description.reattack")}&nbsp;
          {t(
            verificationSummary.onHold > 0 || verificationSummary.requested > 0
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col33>
        <Col33>{permanentlyAccepted}</Col33>
        <Col33 />
      </Row>
    </div>
  );
};

export const renderDescription = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  state,
  treatment,
  verificationSummary,
}: IDescriptionProps): JSX.Element => (
  <Description
    description={description}
    isExploitable={isExploitable}
    lastVulnerability={lastVulnerability}
    openAge={openAge}
    state={state}
    treatment={treatment}
    verificationSummary={verificationSummary}
  />
);
