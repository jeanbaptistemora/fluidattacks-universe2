interface ICommentStructure {
  content: string;
  created: string;
  created_by_current_user: boolean;
  email: string;
  fullname: string;
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
