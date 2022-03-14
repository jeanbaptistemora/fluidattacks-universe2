import { Collapse } from "antd";
import { ErrorMessage, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";

import type { IAffectedAccordionProps, IFinding, IReattackVuln } from "./types";

import type { IFormValues } from "../AddModal";
import { Table } from "components/Table";
import type { IHeaderConfig, ISelectRowProps } from "components/Table/types";
import { ValidationError } from "utils/forms/fields/styles";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;
  const { Panel } = Collapse;
  const { values, setFieldValue, setFieldTouched } =
    useFormikContext<IFormValues>();

  const columns: IHeaderConfig[] = [
    { dataField: "where", header: "Where" },
    { dataField: "specific", header: "Specific" },
  ];

  function onSelect(vuln: IReattackVuln, isSelected: boolean): void {
    setFieldTouched("affectedReattacks", true);
    const selectedId = `${vuln.findingId} ${vuln.id}`;
    if (isSelected) {
      setFieldValue(
        "affectedReattacks",
        _.union(values.affectedReattacks, [selectedId])
      );
    } else {
      setFieldValue(
        "affectedReattacks",
        values.affectedReattacks.filter(
          (item: string): boolean => item !== selectedId
        )
      );
    }
  }

  function onSelectAll(isSelected: boolean, vulns: IReattackVuln[]): void {
    setFieldTouched("affectedReattacks", true);
    const selectedIds = vulns.map(
      (vuln): string => `${vuln.findingId} ${vuln.id}`
    );
    if (isSelected) {
      setFieldValue(
        "affectedReattacks",
        _.union(values.affectedReattacks, selectedIds)
      );
    } else {
      setFieldValue(
        "affectedReattacks",
        values.affectedReattacks.filter(
          (identifier: string): boolean => !selectedIds.includes(identifier)
        )
      );
    }
  }

  const selectionMode: ISelectRowProps = {
    clickToSelect: true,
    mode: "checkbox",
    onSelect,
    onSelectAll,
  };

  const panelOptions = findings.map(
    ({ title, id, vulnerabilitiesToReattack }: IFinding): JSX.Element => {
      if (vulnerabilitiesToReattack.length > 0) {
        return (
          <Panel header={title} key={id}>
            <Table
              dataset={vulnerabilitiesToReattack}
              exportCsv={false}
              headers={columns}
              id={"id"}
              pageSize={10}
              rowSize={"thin"}
              search={false}
              selectionMode={selectionMode}
            />
            <ValidationError>
              <ErrorMessage name={"affectedReattacks"} />
            </ValidationError>
          </Panel>
        );
      }

      return <div key={id} />;
    }
  );

  return (
    <React.StrictMode>
      <Collapse ghost={true}>{panelOptions}</Collapse>
    </React.StrictMode>
  );
};
