interface IOrganizationPortfoliosProps {
  portfolios: IPortfolios[];
}

interface IPortfolios {
  name: string;
  groups: { name: string }[];
}

interface IPortfoliosTable {
  groups: string;
  nGroups: number;
  portfolio: string;
}

export type { IOrganizationPortfoliosProps, IPortfolios, IPortfoliosTable };
