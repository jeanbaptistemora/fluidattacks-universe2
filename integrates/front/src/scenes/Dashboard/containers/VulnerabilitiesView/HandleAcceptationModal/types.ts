interface IVulnDataAttr {
  acceptation: "APPROVED" | "REJECTED";
  id: string;
  specific: string;
  where: string;
}

interface IHandleVulnsAcceptationModalProps {
  findingId: string;
  vulns: IVulnDataAttr[];
  handleCloseModal: () => void;
  refetchData: () => void;
}

interface IHandleVulnsAcceptationResultAttr {
  handleVulnsAcceptation: {
    success: boolean;
  };
}

export {
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IVulnDataAttr,
};
