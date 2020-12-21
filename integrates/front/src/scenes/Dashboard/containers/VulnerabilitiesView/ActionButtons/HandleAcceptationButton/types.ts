export interface IHandleAcceptationButtonProps {
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptation: () => void;
}
