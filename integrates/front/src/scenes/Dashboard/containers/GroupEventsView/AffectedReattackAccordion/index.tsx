import { Collapse } from "antd";
import { Field, useFormikContext } from "formik";
import React from "react";

import type { IAffectedAccordionProps, IFinding, IReattackVuln } from "./types";

import type { IFormValues } from "../AddModal";
import { FormikCheckbox } from "utils/forms/fields";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;
  const { Panel } = Collapse;
  const { setFieldValue } = useFormikContext<IFormValues>();

  const checkAll = (
    findingId: string,
    vulnerabilitiesToReattack: IReattackVuln[]
  ): JSX.Element => {
    function onChange(): void {
      vulnerabilitiesToReattack.forEach(({ id }: IReattackVuln): void => {
        setFieldValue(id, true);
      });
    }

    return (
      <Field
        component={FormikCheckbox}
        key={findingId}
        label={""}
        name={findingId}
        onChange={onChange}
        type={"checkbox"}
      />
    );
  };

  const populatePanel = (): JSX.Element[] => {
    const panelOptions = findings.map(
      ({ title, id, vulnerabilitiesToReattack }: IFinding): JSX.Element => {
        if (vulnerabilitiesToReattack.length > 0) {
          return (
            <Panel
              collapsible={"header"}
              extra={checkAll(id, vulnerabilitiesToReattack)}
              header={title}
              key={id}
            >
              {vulnerabilitiesToReattack.map(
                (vuln: IReattackVuln): JSX.Element => {
                  return (
                    <Field
                      component={FormikCheckbox}
                      key={vuln.id}
                      label={`Where: ${vuln.where} | Spec: ${vuln.specific}`}
                      name={"affectedReattacks"}
                      type={"checkbox"}
                      value={vuln.id}
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
