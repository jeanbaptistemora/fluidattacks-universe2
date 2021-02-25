import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";
import type { IChartsForPortfolioViewProps } from "scenes/Dashboard/containers/ChartsForPortfolioView/types";
import React from "react";
import _ from "lodash";
import { useLocation, useParams } from "react-router";

const ChartsForPortfolioView: React.FC<IChartsForPortfolioViewProps> = (
  props: IChartsForPortfolioViewProps
): JSX.Element => {
  const { tagName } = useParams<{ tagName: string }>();
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );

  const subjectFromSearchParams: string | null = searchParams.get("portfolio");
  const { organizationId } = props;
  const auxOrganizationId: string = _.isUndefined(organizationId)
    ? ""
    : organizationId;
  const subject: string = _.isNull(subjectFromSearchParams)
    ? `${auxOrganizationId}PORTFOLIO#${tagName}`
    : subjectFromSearchParams;

  return (
    <React.StrictMode>
      <ChartsGenericView
        entity={"portfolio"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForPortfolioView };
