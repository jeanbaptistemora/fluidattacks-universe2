interface IVulnData {
  acceptation: "APPROVED" | "REJECTED";
  id: string;
  specific: string;
  where: string;
}

interface IHandleVulnsAcceptationModal {
  findingId: string;
  vulns: IVulnData[];
  handleCloseModal(): void;
  refetchData(): void;
}

interface IHandleVulnsAcceptationResult {
  handleVulnsAcceptation: {
    success: boolean;
  };
}

export { IHandleVulnsAcceptationModal, IHandleVulnsAcceptationResult, IVulnData };
