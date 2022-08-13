interface IRejectDraftModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { reason: string; other: string }) => void;
}

interface IRejectDraftStateProps {
  isRejectDraftModalOpen: boolean;
  openRejectModal: () => void;
  closeRejectModal: () => void;
}

export type { IRejectDraftModalProps, IRejectDraftStateProps };
