interface IGroupTagsAttr {
  group: {
    deletionDate: string;
    name: string;
    subscription: string;
    tags: string[];
  };
}

interface IRemoveTagsAttr {
  removeTag: {
    group: {
      deletionDate: string;
      name: string;
      subscription: string;
      tags: string[];
    };
    success: boolean;
  };
}

interface IAddTagsAttr {
  addGroupTags: {
    group: {
      deletionDate: string;
      name: string;
      subscription: string;
      tags: string[];
    };
    success: boolean;
  };
}

interface IHistoricState {
  date: string;
  state: string;
  user: string;
}

interface IRepositoriesAttr {
  branch: string;
  historicState: IHistoricState[];
  protocol: string;
  state: string;
  urlRepo: string;
}

interface IResourcesAttr {
  resources: {
    environments: string;
    repositories: string;
  };
}

interface IUpdateRepoAttr {
  updateResources: {
    resources: {
      repositories: string;
    };
    success: boolean;
  };
}

interface IAddReposAttr {
  addResources: {
    resources: {
      repositories: string;
    };
    success: boolean;
  };
}

interface IEnvironmentsAttr {
  historicState: IHistoricState[];
  state: string;
  urlEnv: string;
}

interface IUpdateEnvAttr {
  updateResources: {
    resources: {
      environments: string;
    };
    success: boolean;
  };
}

interface IAddEnvAttr {
  addResources: {
    resources: {
      environments: string;
    };
    success: boolean;
  };
}

interface IGetGroupData {
  group: {
    deletionDate: string;
  };
}

export {
  IGroupTagsAttr,
  IRemoveTagsAttr,
  IAddTagsAttr,
  IHistoricState,
  IRepositoriesAttr,
  IResourcesAttr,
  IUpdateRepoAttr,
  IAddReposAttr,
  IEnvironmentsAttr,
  IUpdateEnvAttr,
  IAddEnvAttr,
  IGetGroupData,
};
