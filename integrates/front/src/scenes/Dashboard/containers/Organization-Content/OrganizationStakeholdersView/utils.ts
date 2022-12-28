import type { ExecutionResult } from "graphql";
import _ from "lodash";

import type {
  IRemoveStakeholderResult,
  IStakeholderDataSet,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationStakeholdersView/types";

type IRemoveResult = ExecutionResult<IRemoveStakeholderResult>;

const removeMultipleAccess = async (
  removeStakeholderAccess: (
    variables: Record<string, unknown>
  ) => Promise<IRemoveResult>,
  stakeholders: IStakeholderDataSet[],
  organizationId: string
): Promise<IRemoveResult[]> => {
  const chunkSize = 5;
  const stakeholderChunks = _.chunk(stakeholders, chunkSize);
  const removeChunks = stakeholderChunks.map(
    (chunk): (() => Promise<IRemoveResult[]>) =>
      async (): Promise<IRemoveResult[]> => {
        const updates = chunk.map(
          async (stakeholder): Promise<IRemoveResult> =>
            removeStakeholderAccess({
              variables: { organizationId, userEmail: stakeholder.email },
            })
        );

        return Promise.all(updates);
      }
  );

  return removeChunks.reduce(
    async (previousValue, currentValue): Promise<IRemoveResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<IRemoveResult[]>([])
  );
};

const getAreAllMutationValid = (results: IRemoveResult[]): boolean[] => {
  return results.map((result: IRemoveResult): boolean => {
    if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
      const removeInfoSuccess: boolean = _.isUndefined(
        result.data.removeStakeholderOrganizationAccess
      )
        ? true
        : result.data.removeStakeholderOrganizationAccess.success;

      return removeInfoSuccess;
    }

    return false;
  });
};

export { getAreAllMutationValid, removeMultipleAccess };
