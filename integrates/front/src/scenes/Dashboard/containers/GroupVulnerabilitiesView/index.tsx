import React from "react";
import { useParams } from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";

import { Table } from "components/Table";
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

  return (
    <div>
      <Table
        dataset={vulnerabilities}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblVulnerabilities"}
        pageSize={10}
        search={true}
      />
    </div>
  );
};

export { GroupVulnerabilitiesView };
