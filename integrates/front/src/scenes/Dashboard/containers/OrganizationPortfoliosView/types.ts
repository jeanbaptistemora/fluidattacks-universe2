export interface IOrganizationPortfoliosProps {
  portfolios: IPortfolios[];
}

export interface IPortfolios {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IPortfoliosTable {
    groups: string;
    n_groups: number;
    portfolio: string;
}
