export interface IOrganizationPortfoliosProps {
  portfolios: IPortfolios[];
}

export interface IPortfolios {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IPortfoliosTable {
    name: string;
    projects: string;
}
