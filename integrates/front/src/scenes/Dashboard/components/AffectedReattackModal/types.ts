import type { ExecutionResult } from "graphql";

interface IAffectedVuln {
  affected: boolean;
  findingId: string;
  groupName: string;
  id: string;
  specific: string;
  where: string;
}

interface IUnsolvedEvent {
  description: string;
  detail: string;
  id: string;
  eventStatus: string;
  eventType: string;
}

interface IAffectedReattackModal {
  vulns: IAffectedVuln[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
}

interface IUpdateEventAffectations {
  updateEventAffectations: {
    success: boolean;
  };
}

type UpdateEventAffectationsResult = ExecutionResult<IUpdateEventAffectations>;

export {
  IAffectedVuln,
  UpdateEventAffectationsResult,
  IUnsolvedEvent,
  IAffectedReattackModal,
};
