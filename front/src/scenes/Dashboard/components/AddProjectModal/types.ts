export interface IAddProjectModal {
  isOpen: boolean;
  onClose(): void;
}

export interface IProjectName {
  internalProjectNames: { projectName: string };
}
