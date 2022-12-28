import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router-dom";

import { ChartsView } from "scenes/Dashboard/components/ChartsGenericView";
import type { IChartsForPortfolioViewProps } from "scenes/Dashboard/containers/ChartsForPortfolioView/types";

const ChartsForPortfolioView: React.FC<IChartsForPortfolioViewProps> = ({
  organizationId,
}: IChartsForPortfolioViewProps): JSX.Element => {
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
      <ChartsView
        bgChange={searchParams.get("bgChange") === "true"}
        entity={"portfolio"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForPortfolioView };
