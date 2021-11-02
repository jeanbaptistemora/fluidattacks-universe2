interface ICommentStructure {
  content: string;
  created: string;
  createdByCurrentUser: boolean;
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

export {
  ICommentStructure,
  ICommentContext,
  ICommentsProps,
  ILoadCallback,
  IPostCallback,
};
