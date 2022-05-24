import React from "react";
import { useParams } from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";
import { formatLocation } from "./utils";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";

const tableHeaders: IHeaderConfig[] = [
  {
    dataField: "where",
    formatter: formatLocation,
    header: "Location",
    wrapped: true,
  },
  {
    dataField: "finding.title",
    header: "Type",
    wrapped: true,
  },
  {
    dataField: "reportDate",
    header: "Found",
  },
  {
    dataField: "finding.severityScore",
    header: "Severity",
  },
];

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const vulnerabilities = useGroupVulnerabilities(groupName);

  return (
    <div>
      <Table
        dataset={vulnerabilities}
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
