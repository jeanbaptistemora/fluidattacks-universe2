import React from "react";
import { useParams } from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";
import { filterByState, filterByTreatment, formatLocation } from "./utils";

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
      {[
        { filter: filterByState("open"), title: "Open" },
        { filter: filterByState("closed"), title: "Closed" },
        {
          filter: filterByTreatment("ACCEPTED"),
          title: "Temporarily accepted",
        },
        {
          filter: filterByTreatment("ACCEPTED_UNDEFINED"),
          title: "Permanently accepted",
        },
      ].map(({ title, filter }): JSX.Element => {
        return (
          <section key={title}>
            <h2>{title}</h2>
            <Table
              dataset={vulnerabilities.filter(filter)}
              exportCsv={false}
              headers={tableHeaders}
              id={`tblVulnerabilities${title}`}
              pageSize={10}
              search={false}
            />
          </section>
        );
      })}
    </div>
  );
};

export { GroupVulnerabilitiesView };
