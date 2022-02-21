import type { ExecutionResult } from "graphql";

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
  name: string;
  findings: IFinding[];
}

interface IAffectedReattackModal {
  findings: IReattackVuln[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
}

interface IAffectedAccordionProps {
  findings: IFinding[];
  groupName: string;
}

interface IUpdateEventAffectations {
  updateEventAffectations: {
    success: boolean;
  };
}

type UpdateEventAffectationsResult = ExecutionResult<IUpdateEventAffectations>;

export {
  IAffectedAccordionProps,
  IReattackVuln,
  UpdateEventAffectationsResult,
  IFinding,
  IFindingsQuery,
  IAffectedReattackModal,
};
