import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import type { IChartsForOrganizationViewProps } from "scenes/Dashboard/containers/ChartsForOrganizationView/types";
import React from "react";
import _ from "lodash";
import { useLocation } from "react-router";

const ChartsForOrganizationView: React.FC<IChartsForOrganizationViewProps> = (
  props: IChartsForOrganizationViewProps
): JSX.Element => {
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );
  const { organizationId } = props;
  const maybeOrganizationId: string | null = searchParams.get("organization");

  /*
   * Attempt to read the organization ID from passed Components properties,
   *   or from URL search query, whatever is available first
   */
  const auxOrganizationId: string = _.isUndefined(organizationId)
    ? _.isNull(maybeOrganizationId)
      ? ""
      : maybeOrganizationId
    : organizationId;

  return (
    <React.StrictMode>
      <ChartsGenericView
        entity={"organization"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={auxOrganizationId}
      />
    </React.StrictMode>
  );
};

export { ChartsForOrganizationView };
