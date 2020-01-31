export interface IRemoveProjectModal {
  isOpen: boolean;
  projectName: string;
  onClose(): void;
}

export interface IRemoveProject {
  requestRemoveProject: {
    success: boolean;
  };
}
