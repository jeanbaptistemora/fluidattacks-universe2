import _ from "lodash";
import React from "react";
import { useLocation } from "react-router-dom";

import type { IChartsForOrganizationViewProps } from "scenes/Dashboard/containers/ChartsForOrganizationView/types";
import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";

const ChartsForOrganizationView: React.FC<IChartsForOrganizationViewProps> = ({
  organizationId,
}: IChartsForOrganizationViewProps): JSX.Element => {
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );
  const maybeOrganizationId: string | null = searchParams.get("organization");

  /*
   * Attempt to read the organization ID from passed Components properties,
   *   or from URL search query, whatever is available first
   */
  const auxOrganizationId: string = _.isUndefined(organizationId)
    ? ""
    : organizationId;
  const subject: string = _.isNull(maybeOrganizationId)
    ? auxOrganizationId
    : maybeOrganizationId;

  return (
    <React.StrictMode>
      <ChartsGenericView
        bgChange={searchParams.get("bgChange") === "true"}
        entity={"organization"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForOrganizationView };
