/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Collapse } from "antd";
import { ErrorMessage } from "formik";
import React from "react";

import type { IAffectedAccordionProps, IFinding } from "./types";
import { VulnerabilitiesToReattackTable } from "./VulnerabilitiesToReattackTable";

import { ValidationError } from "utils/forms/fields/styles";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;
  const { Panel } = Collapse;

  const panelOptions = findings.map((finding: IFinding): JSX.Element => {
    if (finding.verified) {
      return <div key={finding.id} />;
    }

    return (
      <Panel header={finding.title} key={finding.id}>
        <VulnerabilitiesToReattackTable finding={finding} />
        <ValidationError>
          <ErrorMessage name={"affectedReattacks"} />
        </ValidationError>
      </Panel>
    );
  });

  return (
    <React.StrictMode>
      <Collapse ghost={true}>{panelOptions}</Collapse>
    </React.StrictMode>
  );
};
