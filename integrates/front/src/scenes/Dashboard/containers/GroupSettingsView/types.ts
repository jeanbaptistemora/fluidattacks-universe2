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

export { IGetFilesQuery, IGetTagsQuery, IGroupFileAttr };
