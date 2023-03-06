interface IGroupBilling {
  costsAuthors: number;
  costsBase: number;
  costsTotal: number;
  numberAuthors: number;
}

interface IOrganizationActiveGroupAttr {
  name: string;
  tier: string;
}

interface IOrganizationAuthorAttr {
  actor: string;
  activeGroups: IOrganizationActiveGroupAttr[];
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

interface IOrganizationBilling {
  costsAuthors: number;
  costsBase: number;
  costsTotal: number;
  numberAuthorsMachine: number;
  numberAuthorsSquad: number;
  numberAuthorsTotal: number;
  numberGroupsMachine: number;
  numberGroupsSquad: number;
  numberGroupsTotal: number;
  paymentMethods: IPaymentMethodAttr[] | undefined;
  portal: string;
}

interface IOrganizationActorAttr {
  name: string;
  email: string;
}

interface IOrganizationAuthorsTable {
  actorName: string;
  actorEmail: string | undefined;
  groupsAuthors: string;
}

interface IGroupAttr {
  billing: IGroupBilling | null;
  forces: string;
  hasForces: boolean;
  hasMachine: boolean;
  hasSquad: boolean;
  machine: string;
  managed: "MANAGED" | "NOT_MANAGED" | "UNDER_REVIEW";
  name: string;
  paymentId: string | null;
  permissions: string[];
  service: string;
  squad: string;
  tier: string;
}

interface IFileMetadata {
  fileName: string;
  modifiedDate: string;
}

interface IGetOrganizationBilling {
  organization: {
    billing: IOrganizationBilling;
    groups: IGroupAttr[];
    name: string;
  };
}

interface IGetOrganizationBillingByDate {
  organization: {
    billing: {
      authors: IOrganizationAuthorAttr[];
    };
    groups: IGroupAttr[];
  };
}

export type {
  IFileMetadata,
  IGetOrganizationBilling,
  IGetOrganizationBillingByDate,
  IGroupAttr,
  IPaymentMethodAttr,
  IOrganizationActorAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
  IOrganizationActiveGroupAttr,
};
