/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IFormValues {
  port: string;
  rootId: string;
}

interface IAddToePortResultAttr {
  addToePort: {
    success: boolean;
  };
}

interface IHandleAdditionModalProps {
  groupName: string;
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IGitRootAttr {
  __typename: "GitRoot";
}

interface IIPRootAttr {
  __typename: "IPRoot";
  address: string;
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IURLRootAttr {
  __typename: "URLRoot";
}

type Root = IGitRootAttr | IIPRootAttr | IURLRootAttr;

export type {
  IFormValues,
  IHandleAdditionModalProps,
  IAddToePortResultAttr,
  Root,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
};
