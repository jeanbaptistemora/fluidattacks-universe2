import { Collapse } from "antd";
import { ErrorMessage, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import type { SelectRowProps } from "react-bootstrap-table-next";
import BootstrapTable from "react-bootstrap-table-next";

import type { IAffectedAccordionProps, IFinding, IReattackVuln } from "./types";

import type { IFormValues } from "../AddModal";
import style from "components/DataTableNext/index.css";
import { ValidationError } from "utils/forms/fields/styles";

export const AffectedReattackAccordion: React.FC<IAffectedAccordionProps> = (
  props: IAffectedAccordionProps
): JSX.Element => {
  const { findings } = props;
  const { Panel } = Collapse;
  const { values, setFieldValue, setFieldTouched } =
    useFormikContext<IFormValues>();

  const columns = [
    { align: "center", dataField: "where", text: "Where" },
    {
      align: "center",
      dataField: "specific",
      text: "Specific",
    },
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

  const selectRow: SelectRowProps<IReattackVuln> = {
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
            <BootstrapTable
              bootstrap4={true}
              columns={columns}
              data={vulnerabilitiesToReattack}
              keyField={"id"}
              selectRow={selectRow}
              wrapperClasses={`f6 mw-100 overflow-auto ${style.tableWrapper}`}
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
