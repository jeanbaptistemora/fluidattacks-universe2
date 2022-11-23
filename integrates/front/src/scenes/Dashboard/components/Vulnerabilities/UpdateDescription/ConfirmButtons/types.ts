interface IConfirmButtonsProps {
  deletingTag: boolean;
  handleCloseModal: () => void;
  isDescriptionPristine: boolean;
  isRunning: boolean;
  isTreatmentDescriptionPristine: boolean;
  isTreatmentPristine: boolean;
  requestingZeroRisk: boolean;
  updatingVulnerability: boolean;
}

export type { IConfirmButtonsProps };
