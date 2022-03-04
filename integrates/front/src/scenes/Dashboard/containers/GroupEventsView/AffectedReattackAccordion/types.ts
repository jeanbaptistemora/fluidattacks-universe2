interface IReattackVuln {
  affected?: boolean;
  findingId: string;
  id: string;
  specific: string;
  where: string;
}

interface IFinding {
  id: string;
  title: string;
  vulnerabilitiesToReattack: IReattackVuln[];
}

interface IFindingsQuery {
  group: {
    name: string;
    findings: IFinding[];
  };
}

interface IAffectedReattackModal {
  findings: IReattackVuln[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
}

interface IAffectedAccordionProps {
  findings: IFinding[];
}

interface IUpdateEventAffectations {
  updateEventAffectations: {
    success: boolean;
  };
}

export {
  IAffectedAccordionProps,
  IReattackVuln,
  IFinding,
  IFindingsQuery,
  IAffectedReattackModal,
  IUpdateEventAffectations,
};
