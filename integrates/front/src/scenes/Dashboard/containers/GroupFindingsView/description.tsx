import React from "react";
import { useTranslation } from "react-i18next";

import type { IFindingData } from "./types";

import { Col50, Row } from "styles/styledComponents";

interface IDescriptionProps {
  description: string;
  isExploitable: boolean;
  lastVulnerability: number;
  openAge: number;
  remediated: string;
  treatment: string;
}

const Description = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  remediated,
  treatment,
}: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const [treatmentNew, inProgress, temporallyAccepted, permanentlyAccepted] =
    treatment.split(",").map((line): string => line.trim());

  return (
    <div>
      <h3>{t("group.findings.description.title")}</h3>
      <Row>
        <p>{description}</p>
      </Row>
      <Row>
        <Col50>
          {t("group.findings.description.lastReport")}&nbsp;
          {t("group.findings.description.value", { count: lastVulnerability })}
        </Col50>
        <Col50>{treatmentNew}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.findings.description.firstSeen")}&nbsp;
          {t("group.findings.description.value", { count: openAge })}
        </Col50>
        <Col50>{inProgress}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.findings.description.exploitable")}&nbsp;
          {t(
            isExploitable
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col50>
        <Col50>{temporallyAccepted}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>
          {t("group.findings.description.reattack")}&nbsp;
          {t(
            remediated === "Pending"
              ? "group.findings.boolean.True"
              : "group.findings.boolean.False"
          )}
        </Col50>
        <Col50>{permanentlyAccepted}</Col50>
      </Row>
    </div>
  );
};

export const renderDescription = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  remediated,
  treatment,
}: IFindingData): JSX.Element => (
  <Description
    description={description}
    isExploitable={isExploitable}
    lastVulnerability={lastVulnerability}
    openAge={openAge}
    remediated={remediated}
    treatment={treatment}
  />
);
