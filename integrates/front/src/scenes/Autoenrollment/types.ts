/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAddOrganizationResult {
  addOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

type IAlertMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

interface ICheckGitAccessResult {
  validateGitAccess: {
    success: boolean;
  };
}

interface IRootAttr {
  branch: string;
  credentials: {
    auth: "TOKEN" | "USER";
    id: string;
    key: string;
    name: string;
    password: string;
    token: string;
    type: "" | "HTTPS" | "SSH";
    user: string;
  };
  env: string;
  exclusions: string[];
  url: string;
}

interface IOrgAttr {
  groupDescription: string;
  groupName: string;
  organizationName: string;
  reportLanguage: string;
  terms: string[];
}

export type {
  IAddOrganizationResult,
  IAlertMessages,
  ICheckGitAccessResult,
  IOrgAttr,
  IRootAttr,
};
