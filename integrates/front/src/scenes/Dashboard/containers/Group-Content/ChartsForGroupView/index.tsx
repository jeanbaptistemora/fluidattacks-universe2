import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router-dom";

import { ChartsView } from "scenes/Dashboard/components/ChartsGenericView";

const ChartsForGroupView: React.FC = (): JSX.Element => {
  const params: { groupName: string } = useParams();
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );

  const subjectFromSearchParams: string | null = searchParams.get("group");

  const subject: string = _.isNull(subjectFromSearchParams)
    ? params.groupName
    : subjectFromSearchParams;

  return (
    <React.StrictMode>
      <ChartsView
        bgChange={searchParams.get("bgChange") === "true"}
        entity={"group"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForGroupView };
