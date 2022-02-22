import { Collapse } from "antd";
import { Field } from "formik";
import React from "react";

import type { IAffectedAccordionProps, IFinding, IReattackVuln } from "./types";

import { FormikCheckbox } from "utils/forms/fields";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;
  const { Panel } = Collapse;

  const populatePanel = (): JSX.Element[] => {
    const panelOptions = findings.map(
      ({ title, id, vulnerabilitiesToReattack }: IFinding): JSX.Element => {
        if (vulnerabilitiesToReattack.length > 0) {
          return (
            <Panel header={title} key={id}>
              {vulnerabilitiesToReattack.map(
                (vuln: IReattackVuln): JSX.Element => {
                  return (
                    <Field
                      component={FormikCheckbox}
                      key={vuln.id}
                      label={`Where: ${vuln.where} | Spec: ${vuln.specific}`}
                      name={vuln.id}
                      type={"checkbox"}
                    />
                  );
                }
              )}
            </Panel>
          );
        }

        return <div key={id} />;
      }
    );

    return panelOptions;
  };

  return (
    <React.StrictMode>
      <Collapse ghost={true}>{populatePanel()}</Collapse>
    </React.StrictMode>
  );
};
