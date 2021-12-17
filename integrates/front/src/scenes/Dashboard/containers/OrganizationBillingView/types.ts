interface IBillingData {
  name: string;
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
