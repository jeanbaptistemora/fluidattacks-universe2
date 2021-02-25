import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import React from "react";
import _ from "lodash";
import { useLocation, useParams } from "react-router";

const ChartsForGroupView: React.FC = (): JSX.Element => {
  const params: { projectName: string } = useParams();
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );

  const subjectFromSearchParams: string | null = searchParams.get("group");

  const subject: string = _.isNull(subjectFromSearchParams)
    ? params.projectName
    : subjectFromSearchParams;

  return (
    <React.StrictMode>
      <ChartsGenericView
        entity={"group"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForGroupView };
