import type { ExecutionResult } from "graphql";

interface IUpdateEventAffectations {
  updateEventAffectations: {
    success: boolean;
  };
}

export type UpdateEventAffectationsResult =
  ExecutionResult<IUpdateEventAffectations>;
