interface IGroupAuthors {
  currentSpend: number;
  total: number;
}

interface IGroupAttr {
  authors: IGroupAuthors | null;
  forces: string;
  hasForces: boolean;
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  managed: "MANAGED" | "NOT_MANAGED" | "UNDER_REVIEW";
  name: string;
  permissions: string[];
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
  businessName: string;
  email: string;
  country: string;
  state: string;
  city: string;
  rut: File | undefined;
  taxId: File | undefined;
}

interface IGetOrganizationBilling {
  organization: {
    billingPortal: string;
    groups: IGroupAttr[];
    paymentMethods: IPaymentMethodAttr[];
  };
}

export type { IGetOrganizationBilling, IGroupAttr, IPaymentMethodAttr };
