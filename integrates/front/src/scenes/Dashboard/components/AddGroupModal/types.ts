interface IAddGroupModalProps {
  isOpen: boolean;
  organization: string;
  onClose: () => void;
}

interface IGroupNameProps {
  internalNames: { name: string };
}

export { IAddGroupModalProps, IGroupNameProps };
