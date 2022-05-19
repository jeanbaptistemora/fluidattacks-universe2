import React from "react";
import { useParams } from "react-router-dom";

import { useGroupVulnerabilities } from "./hooks";

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const vulnerabilities = useGroupVulnerabilities(groupName);

  return <div>{JSON.stringify(vulnerabilities)}</div>;
};

export { GroupVulnerabilitiesView };
