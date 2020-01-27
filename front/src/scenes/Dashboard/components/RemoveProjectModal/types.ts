export interface IRemoveProjectModal {
  isOpen: boolean;
  projectName: string;
  onClose(): void;
}

export interface IRemoveProject {
  removeProject: {
    findingsMasked: boolean;
    projectFinished: boolean;
    success: boolean;
    usersRemoved: boolean;
  };
}
