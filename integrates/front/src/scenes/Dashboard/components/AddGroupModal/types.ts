interface IAddProjectModalProps {
  isOpen: boolean;
  organization: string;
  onClose: () => void;
}

interface IProjectNameProps {
  internalNames: { name: string };
}

export { IAddProjectModalProps, IProjectNameProps };
