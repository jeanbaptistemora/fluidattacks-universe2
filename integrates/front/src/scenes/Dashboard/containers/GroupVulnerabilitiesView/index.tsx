import { useQuery } from "@apollo/client";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_GROUP_FINDINGS } from "./queries";
import type { IGroupFindings } from "./types";

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { data } = useQuery<IGroupFindings>(GET_GROUP_FINDINGS, {
    variables: { groupName },
  });
  const findings = data === undefined ? [] : data.group.findings;

  return <div>{JSON.stringify(findings)}</div>;
};

export { GroupVulnerabilitiesView };
