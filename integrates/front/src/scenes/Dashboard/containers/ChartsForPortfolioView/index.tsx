/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React, { useContext } from "react";
import { useLocation, useParams } from "react-router-dom";

import type { IChartsForPortfolioViewProps } from "scenes/Dashboard/containers/ChartsForPortfolioView/types";
import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import { ChartsChangedOrderView } from "scenes/Dashboard/containers/ChartsGenericView/newOrderIndex";
import { featurePreviewContext } from "utils/featurePreview";

const ChartsForPortfolioView: React.FC<IChartsForPortfolioViewProps> = ({
  organizationId,
}: IChartsForPortfolioViewProps): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);
  const { tagName } = useParams<{ tagName: string }>();
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );

  const subjectFromSearchParams: string | null = searchParams.get("portfolio");
  const auxOrganizationId: string = _.isUndefined(organizationId)
    ? ""
    : organizationId;
  const subject: string = _.isNull(subjectFromSearchParams)
    ? `${auxOrganizationId}PORTFOLIO#${tagName}`
    : subjectFromSearchParams;

  return (
    <React.StrictMode>
      {featurePreview ? (
        <ChartsChangedOrderView
          bgChange={searchParams.get("bgChange") === "true"}
          entity={"portfolio"}
          reportMode={searchParams.get("reportMode") === "true"}
          subject={subject}
        />
      ) : (
        <ChartsGenericView
          bgChange={searchParams.get("bgChange") === "true"}
          entity={"portfolio"}
          reportMode={searchParams.get("reportMode") === "true"}
          subject={subject}
        />
      )}
    </React.StrictMode>
  );
};

export { ChartsForPortfolioView };
