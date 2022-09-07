/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupAuthor {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IData {
  group: {
    authors: {
      data: IGroupAuthor[];
    };
  };
}

interface IAuthors extends IGroupAuthor {
  invitation: JSX.Element;
}

export type { IAuthors, IGroupAuthor, IData };
