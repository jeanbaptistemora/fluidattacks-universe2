function getInitialTreatment(
  canHandleVulnsAccept: boolean,
  canConfirmVulnerability: boolean,
  canConfirmZeroRisk: boolean
): string {
  if (canHandleVulnsAccept) {
    return "ACCEPTED_UNDEFINED";
  } else if (canConfirmVulnerability) {
    return "CONFIRM_REJECT_VULNERABILITY";
  } else if (canConfirmZeroRisk) {
    return "CONFIRM_REJECT_ZERO_RISK";
  }

  return "";
}

export { getInitialTreatment };
