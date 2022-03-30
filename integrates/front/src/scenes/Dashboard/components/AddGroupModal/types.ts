interface IAddGroupModalProps {
  isOpen: boolean;
  organization: string;
  onClose: () => void;
  runTour: boolean;
}

interface IGroupNameProps {
  internalNames: { name: string };
}

export { IAddGroupModalProps, IGroupNameProps };
