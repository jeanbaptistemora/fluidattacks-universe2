import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router";
import { IChartsForPortfolioViewProps } from "scenes/Dashboard/containers/ChartsForPortfolioView/types";
import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";

const chartsForPortfolioView: React.FC<IChartsForPortfolioViewProps> = (
  props: IChartsForPortfolioViewProps,
): JSX.Element => {
  const { tagName } = useParams<{ tagName: string }>();
  const searchParams: URLSearchParams = new URLSearchParams(useLocation().search);

  const subjectFromSearchParams: string | null = searchParams.get("portfolio");

  const organizationId: string = _.isUndefined(props.organizationId) ? "" : props.organizationId;
  const subject: string = _.isNull(subjectFromSearchParams)
  ? `${organizationId}PORTFOLIO#${tagName}` : subjectFromSearchParams;

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

export { chartsForPortfolioView as ChartsForPortfolioView };
