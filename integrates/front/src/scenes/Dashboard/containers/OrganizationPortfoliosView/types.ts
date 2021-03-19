interface IOrganizationPortfoliosProps {
  portfolios: IPortfolios[];
}

interface IPortfolios {
  name: string;
  projects: { name: string }[];
}

interface IPortfoliosTable {
  groups: string;
  nGroups: number;
  portfolio: string;
}

export { IOrganizationPortfoliosProps, IPortfolios, IPortfoliosTable };
