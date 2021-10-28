export interface IHandleAcceptanceButtonProps {
  areVulnerabilitiesPendingToAcceptance: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptance: () => void;
}
