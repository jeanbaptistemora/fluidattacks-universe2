interface IGetFilesQuery {
  resources: {
    files: string;
  };
}

interface IGetTagsQuery {
  group: {
    name: string;
    tags: string[] | null;
  };
}

export { IGetFilesQuery, IGetTagsQuery };
