export interface IAddProjectModal {
  isOpen: boolean;
  organization: string;
  onClose(): void;
}

export interface IProjectName {
  internalProjectNames: { projectName: string };
}
