import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router";
import { ChartsGenericView } from "../ChartsGenericView";

const chartsForGroupView: React.FC = (): JSX.Element => {
  const params: { projectName: string } = useParams();
  const searchParams: URLSearchParams = new URLSearchParams(useLocation().search);

  const subjectFromSearchParams: string | null = searchParams.get("group");

  const subject: string = _.isNull(subjectFromSearchParams) ? params.projectName : subjectFromSearchParams;

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

export { chartsForGroupView as ChartsForGroupView };
