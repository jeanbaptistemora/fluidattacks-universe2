import { ErrorMessage } from "formik";
import React from "react";

import type { IAffectedAccordionProps, IFinding } from "./types";
import { VulnerabilitiesToReattackTable } from "./VulnerabilitiesToReattackTable";

import { Accordion } from "components/Accordion";
import { ValidationError } from "utils/forms/fields/styles";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;

  const panelOptions = findings.map((finding: IFinding): JSX.Element => {
    if (finding.verified) {
      return <div key={finding.id} />;
    }

    return (
      <Accordion header={finding.title} initCollapsed={true} key={finding.id}>
        <VulnerabilitiesToReattackTable finding={finding} />
        <ValidationError>
          <ErrorMessage name={"affectedReattacks"} />
        </ValidationError>
      </Accordion>
    );
  });

  return (
    <React.StrictMode>
      <div>{panelOptions}</div>
    </React.StrictMode>
  );
};
