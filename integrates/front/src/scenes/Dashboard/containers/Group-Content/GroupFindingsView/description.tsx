import React from "react";
import { useTranslation } from "react-i18next";

import type { IVerificationSummaryAttr } from "./types";

import { Col, Row } from "components/Layout";

interface IDescriptionProps {
  description: string;
  isExploitable: boolean;
  lastVulnerability: number;
  openAge: number;
  status: "SAFE" | "VULNERABLE";
  treatment: string;
  verificationSummary: IVerificationSummaryAttr;
}

const Description = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  status,
  treatment,
  verificationSummary,
}: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const [treatmentNew, inProgress, temporallyAccepted, permanentlyAccepted] =
    treatment.split(",").map((line): string => line.trim());
  const isOpen = status === "VULNERABLE";

  return (
    <div>
      <h3>{t("group.findings.description.title")}</h3>
      <Row>
        <p>{description}</p>
      </Row>
      <Row>
        <Col>
          {t("group.findings.description.lastReport")}&nbsp;
          {t("group.findings.description.value", { count: lastVulnerability })}
        </Col>
        <Col>{treatmentNew}</Col>
        {isOpen ? (
          <Col>
            {t("group.findings.description.onHold")}&nbsp;
            {verificationSummary.onHold}
          </Col>
        ) : (
          <Col />
        )}
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.findings.description.firstSeen")}&nbsp;
          {t("group.findings.description.value", { count: openAge })}
        </Col>
        <Col>{inProgress}</Col>
        {isOpen ? (
          <Col>
            {t("group.findings.description.requested")}&nbsp;
            {verificationSummary.requested}
          </Col>
        ) : (
          <Col />
        )}
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.findings.description.exploitable")}&nbsp;
          {t(
            isExploitable
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col>
        <Col>{temporallyAccepted}</Col>
        {isOpen ? (
          <Col>
            {t("group.findings.description.verified")}&nbsp;
            {verificationSummary.verified}
          </Col>
        ) : (
          <Col />
        )}
      </Row>
      <hr />
      <Row>
        <Col>
          {t("group.findings.description.reattack")}&nbsp;
          {t(
            verificationSummary.onHold > 0 || verificationSummary.requested > 0
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col>
        <Col>{permanentlyAccepted}</Col>
        <Col />
      </Row>
    </div>
  );
};

export const renderDescription = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  status,
  treatment,
  verificationSummary,
}: IDescriptionProps): JSX.Element => (
  <Description
    description={description}
    isExploitable={isExploitable}
    lastVulnerability={lastVulnerability}
    openAge={openAge}
    status={status}
    treatment={treatment}
    verificationSummary={verificationSummary}
  />
);
