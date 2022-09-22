/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React, { useContext } from "react";
import { useLocation } from "react-router-dom";

import type { IChartsForOrganizationViewProps } from "scenes/Dashboard/containers/ChartsForOrganizationView/types";
import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import { ChartsChangedOrderView } from "scenes/Dashboard/containers/ChartsGenericView/newOrderIndex";
import { featurePreviewContext } from "utils/featurePreview";

const ChartsForOrganizationView: React.FC<IChartsForOrganizationViewProps> = ({
  organizationId,
}: IChartsForOrganizationViewProps): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);
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
      {featurePreview ? (
        <ChartsChangedOrderView
          bgChange={searchParams.get("bgChange") === "true"}
          entity={"organization"}
          reportMode={searchParams.get("reportMode") === "true"}
          subject={subject}
        />
      ) : (
        <ChartsGenericView
          bgChange={searchParams.get("bgChange") === "true"}
          entity={"organization"}
          reportMode={searchParams.get("reportMode") === "true"}
          subject={subject}
        />
      )}
    </React.StrictMode>
  );
};

export { ChartsForOrganizationView };
