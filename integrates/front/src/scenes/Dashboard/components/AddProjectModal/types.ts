export interface IAddProjectModal {
  isOpen: boolean;
  organization: string;
  onClose(): void;
}

export interface IProjectName {
  internalNames: { name: string };
}
