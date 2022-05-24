import React from "react";
import { useParams } from "react-router-dom";

import { renderDescription } from "./description";
import { useGroupVulnerabilities } from "./hooks";

import { Table } from "components/Table";
import { useRowExpand } from "components/Table/hooks/useRowExpand";
import type { IHeaderConfig } from "components/Table/types";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "where",
    header: "Where",
    wrapped: true,
  },
  {
    dataField: "specific",
    header: "Specific",
  },
];

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const vulnerabilities = useGroupVulnerabilities(groupName);

  const { expandedRows, handleRowExpand, handleRowExpandAll } = useRowExpand({
    rowId: "id",
    rows: vulnerabilities,
    storageKey: "vulnerabilityExpandedRows",
  });

  return (
    <div>
      <Table
        dataset={vulnerabilities}
        expandRow={{
          expandByColumnOnly: true,
          expanded: expandedRows,
          onExpand: handleRowExpand,
          onExpandAll: handleRowExpandAll,
          renderer: renderDescription,
          showExpandColumn: true,
        }}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblVulnerabilities"}
        pageSize={10}
        search={false}
      />
    </div>
  );
};

export { GroupVulnerabilitiesView };
