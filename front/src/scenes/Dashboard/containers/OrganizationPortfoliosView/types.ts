export interface IOrganizationPortfoliosProps {
  organizationId: string;
}

export interface IPortfolios {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IPortfoliosTable {
    name: string;
    projects: string;
}
