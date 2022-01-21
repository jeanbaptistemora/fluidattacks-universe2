interface IBillingData {
  forces: string;
  hasForces: boolean;
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  name: string;
  service: string;
  squad: string;
  tier: string;
}

interface IOrganizationBillingProps {
  organizationId: string;
}

interface IGetOrganizationBilling {
  organization: {
    groups: IBillingData[];
  };
}

export { IBillingData, IGetOrganizationBilling, IOrganizationBillingProps };
