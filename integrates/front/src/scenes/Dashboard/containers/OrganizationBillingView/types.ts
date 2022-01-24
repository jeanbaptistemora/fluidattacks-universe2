interface IGroupAttr {
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

interface IPaymentMethodAttr {
  id: string;
  brand: string;
  default: boolean;
  lastFourDigits: string;
  expirationMonth: string;
  expirationYear: string;
}

interface IOrganizationBillingProps {
  organizationId: string;
}

interface IGetOrganizationBilling {
  organization: {
    groups: IGroupAttr[];
    billingPaymentMethods: IPaymentMethodAttr[];
  };
}

export {
  IGroupAttr,
  IPaymentMethodAttr,
  IGetOrganizationBilling,
  IOrganizationBillingProps,
};
