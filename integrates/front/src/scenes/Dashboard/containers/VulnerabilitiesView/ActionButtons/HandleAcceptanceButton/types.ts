export interface IHandleAcceptanceButtonProps {
  areVulnerabilitiesPendingToAcceptation: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptation: () => void;
}
