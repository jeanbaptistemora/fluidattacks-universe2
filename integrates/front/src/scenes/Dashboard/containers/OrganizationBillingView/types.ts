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
  managed: "MANUALLY" | "NOT_MANUALLY" | "UNDER_REVIEW";
  name: string;
  permissions: string[];
  service: string;
  squad: string;
  tier: string;
}

interface IFileMetadata {
  fileName: string;
  modifiedDate: string;
}

interface IPaymentMethodAttr {
  id: string;
  brand: string;
  default: boolean;
  lastFourDigits: string;
  expirationMonth: string;
  expirationYear: string;
  businessName: string;
  download: string;
  email: string;
  country: string;
  state: string;
  city: string;
  rut: IFileMetadata | undefined;
  taxId: IFileMetadata | undefined;
}

interface IGetOrganizationBilling {
  organization: {
    billingPortal: string;
    groups: IGroupAttr[];
    paymentMethods: IPaymentMethodAttr[];
  };
}

export type {
  IFileMetadata,
  IGetOrganizationBilling,
  IGroupAttr,
  IPaymentMethodAttr,
};
