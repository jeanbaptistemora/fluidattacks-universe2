import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router";
import { ChartsGenericView } from "../ChartsGenericView";
import { IChartsForOrganizationViewProps } from "./types";

const chartsForOrganizationView: React.FC<IChartsForOrganizationViewProps> = (
  props: IChartsForOrganizationViewProps,
): JSX.Element => {
  const { organizationId } = props;

  const searchParams: URLSearchParams = new URLSearchParams(useLocation().search);

  return (
    <React.StrictMode>
      <ChartsGenericView
        entity={"organization"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={organizationId}
      />
    </React.StrictMode>
  );
};

export { chartsForOrganizationView as ChartsForOrganizationView };
