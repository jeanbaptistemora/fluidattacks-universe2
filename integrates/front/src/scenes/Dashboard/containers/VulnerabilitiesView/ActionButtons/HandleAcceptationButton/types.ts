export interface IHandleAcceptationButtonProps {
  canHandleAcceptation: boolean;
  isConfirmingZeroRisk: boolean;
  isEditing: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptation: () => void;
}
