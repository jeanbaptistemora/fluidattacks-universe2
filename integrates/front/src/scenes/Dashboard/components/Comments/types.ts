interface ICommentStructure {
  content: string;
  created: string;
  // eslint-disable-next-line camelcase -- It is possibly required for the API
  created_by_current_user: boolean;
  email: string;
  fullName: string;
  id: number;
  modified: string;
  parent: number;
}

interface ILoadCallback {
  (comments: ICommentStructure[]): void;
}

interface IPostCallback {
  (comments: ICommentStructure): void;
}

interface ICommentsProps {
  id: string;
  onLoad: (callbackFn: (comments: ICommentStructure[]) => void) => void;
  onPostComment: (
    comment: ICommentStructure,
    callbackFn: (comments: ICommentStructure) => void
  ) => void;
}

export { ICommentStructure, ICommentsProps, ILoadCallback, IPostCallback };
