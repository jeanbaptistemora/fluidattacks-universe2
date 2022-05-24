import React from "react";

import type { IVulnerability } from "./types";

interface IDescriptionProps {
  vulnerability: IVulnerability;
}

const Description = ({ vulnerability }: IDescriptionProps): JSX.Element => {
  return (
    <div>
      <h3>{"Types"}</h3>
      <ul>
        {vulnerability.findings.map(
          (finding): JSX.Element => (
            <li key={finding.id}>{finding.title}</li>
          )
        )}
      </ul>
    </div>
  );
};

export const renderDescription = (
  vulnerability: IVulnerability
): JSX.Element => <Description vulnerability={vulnerability} />;
