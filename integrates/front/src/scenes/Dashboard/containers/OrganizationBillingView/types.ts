/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupBilling {
  currentSpend: number;
  total: number;
}

interface IOrganizationAuthorAttr {
  actor: string;
  groups: string[];
}

interface IOrganizationBilling {
  currentSpend: number;
  authors: IOrganizationAuthorAttr[];
  total: number;
  portal: string;
}

interface IOrganizationAuthorsTable {
  actor: string;
  groups: string;
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
    billing: IOrganizationBilling;
    groups: IGroupAttr[];
    paymentMethods: IPaymentMethodAttr[] | undefined;
  };
}

export type {
  IFileMetadata,
  IGetOrganizationBilling,
  IGroupAttr,
  IPaymentMethodAttr,
  IOrganizationAuthorAttr,
  IOrganizationAuthorsTable,
};
