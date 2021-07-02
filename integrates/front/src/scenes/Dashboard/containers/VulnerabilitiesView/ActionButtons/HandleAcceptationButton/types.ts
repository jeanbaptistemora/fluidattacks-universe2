export interface IHandleAcceptationButtonProps {
  areVulnerabilitiesPendingToAcceptation: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptation: () => void;
}
