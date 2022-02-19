import type { ExecutionResult } from "graphql";

interface IReattackVuln {
  affected?: boolean;
  findingId: string;
  id: string;
  specific: string;
  where: string;
}

interface IEvent {
  detail: string;
  id: string;
  eventStatus: string;
  eventType: string;
}

interface IEventsQuery {
  group: { events: IEvent[] };
}

interface IAffectedReattackModal {
  vulns: IReattackVuln[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
}

interface IAffectedAccordionProps {
  findings: string[];
  vulnerabilities: IReattackVuln[];
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
  IEvent,
  IEventsQuery,
  IAffectedReattackModal,
};
