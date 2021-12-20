interface IBillingData {
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  name: string;
  service: string;
  squad: string;
  subscription: string;
}

interface IOrganizationBillingProps {
  organizationId: string;
}

interface IGetOrganizationBilling {
  organization: {
    groups: IBillingData[];
  };
}

export { IBillingData, IOrganizationBillingProps, IGetOrganizationBilling };
