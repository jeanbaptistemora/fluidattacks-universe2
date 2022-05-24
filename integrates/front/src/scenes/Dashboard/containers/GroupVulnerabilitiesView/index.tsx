import React from "react";
import { useParams } from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";
import { formatLocation, formatType } from "./utils";

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
    dataField: "findings",
    formatter: formatType,
    header: "Type",
    wrapped: true,
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
