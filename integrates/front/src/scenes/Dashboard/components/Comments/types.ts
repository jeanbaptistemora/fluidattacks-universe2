/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ICommentStructure {
  content: string;
  created: string;
  createdByCurrentUser: boolean;
  email: string;
  fullName: string;
  id: number;
  modified: string;
  parentComment: number;
}

interface ILoadCallback {
  (comments: ICommentStructure[]): void;
}

interface IPostCallback {
  (comments: ICommentStructure): void;
}

interface ICommentsProps {
  onLoad: (callbackFn: ILoadCallback) => void;
  onPostComment: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void;
}

interface ICommentContext {
  replying: number;
  setReplying?: React.Dispatch<React.SetStateAction<number>>;
}

export type {
  ICommentStructure,
  ICommentContext,
  ICommentsProps,
  ILoadCallback,
  IPostCallback,
};
