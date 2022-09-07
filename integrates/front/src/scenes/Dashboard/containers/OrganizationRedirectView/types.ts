/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IOrganizationRedirectProps {
  type: string;
}

interface IGetEntityOrganization {
  group?: {
    name: string;
    organization: string;
  };
  tag?: {
    organization: string;
  };
}

export type { IGetEntityOrganization, IOrganizationRedirectProps };
