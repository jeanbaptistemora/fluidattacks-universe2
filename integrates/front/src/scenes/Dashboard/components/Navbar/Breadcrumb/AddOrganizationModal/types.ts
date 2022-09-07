/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAddOrganizationModalProps {
  open: boolean;
  onClose: () => void;
}

interface IAddOrganizationMtProps {
  addOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

export type { IAddOrganizationModalProps, IAddOrganizationMtProps };
