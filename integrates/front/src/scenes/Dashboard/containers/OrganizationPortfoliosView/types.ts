/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IOrganizationPortfoliosProps {
  portfolios: IPortfolios[];
}

interface IPortfolios {
  name: string;
  groups: { name: string }[];
}

interface IPortfoliosTable {
  groups: string;
  nGroups: number;
  portfolio: string;
}

export type { IOrganizationPortfoliosProps, IPortfolios, IPortfoliosTable };
