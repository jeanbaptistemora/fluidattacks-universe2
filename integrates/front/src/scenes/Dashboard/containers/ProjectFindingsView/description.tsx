import React from "react";

import { Col50, Row } from "styles/styledComponents";

interface IDescriptionProps {
  description: string;
  isExploitable: boolean;
  lastVulnerability: string;
  openAge: string;
  remediated: string;
  treatment: string;
}

export const Description = ({
  description,
  isExploitable,
  lastVulnerability,
  openAge,
  remediated,
  treatment,
}: IDescriptionProps): JSX.Element => {
  const [
    treatmentNew,
    inProgress,
    temporallyAccepted,
    eternallyAccepted,
  ] = treatment.split(",").map((line): string => line.trim());

  return (
    <div>
      <Row>
        <p>{description}</p>
      </Row>
      <Row>
        <Col50>{lastVulnerability}</Col50>
        <Col50>{treatmentNew}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>{openAge}</Col50>
        <Col50>{inProgress}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>{isExploitable ? "yes" : "no"}</Col50>
        <Col50>{temporallyAccepted}</Col50>
      </Row>
      <hr />
      <Row>
        <Col50>{remediated === "Pending" ? "yes" : "no"}</Col50>
        <Col50>{eternallyAccepted}</Col50>
      </Row>
    </div>
  );
};
