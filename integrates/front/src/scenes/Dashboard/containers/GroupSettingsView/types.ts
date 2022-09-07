/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IGroupFileAttr {
  description: string;
  uploader: string;
  uploadDate: string | null;
  fileName: string;
}
interface IGetFilesQuery {
  resources: {
    files: IGroupFileAttr[] | null;
  };
}

interface IGetTagsQuery {
  group: {
    name: string;
    tags: string[] | null;
  };
}

export type { IGetFilesQuery, IGetTagsQuery, IGroupFileAttr };
