import _ from "lodash";
import React from "react";
import { useLocation } from "react-router";
import { ChartsGenericView } from "../ChartsGenericView";
import { IChartsForOrganizationViewProps } from "./types";

const chartsForOrganizationView: React.FC<IChartsForOrganizationViewProps> = (
  props: IChartsForOrganizationViewProps,
): JSX.Element => {
  const searchParams: URLSearchParams = new URLSearchParams(useLocation().search);

  const maybeOrganizationId: string | null = searchParams.get("organization");
  const organizationId: string = _.isUndefined(props.organizationId)
    ? (_.isNull(maybeOrganizationId) ? "" : maybeOrganizationId)
    : props.organizationId;

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
