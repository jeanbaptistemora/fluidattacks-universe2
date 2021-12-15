interface IGetFilesQuery {
  resources: {
    files: string;
  };
}

interface IGetTagsQuery {
  group: {
    name: string;
    tags: string[];
  };
}

export { IGetFilesQuery, IGetTagsQuery };
