function getInitialTreatment(
  canHandleVulnsAccept: boolean,
  canConfirmZeroRisk: boolean
): string {
  if (canHandleVulnsAccept) {
    return "ACCEPTED_UNDEFINED";
  }

  return canConfirmZeroRisk ? "CONFIRM_REJECT_ZERO_RISK" : "";
}

export { getInitialTreatment };
