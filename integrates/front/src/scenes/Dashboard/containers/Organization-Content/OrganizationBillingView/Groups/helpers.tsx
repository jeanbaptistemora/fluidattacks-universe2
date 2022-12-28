import type { ExecutionResult } from "graphql/execution";
import _ from "lodash";

import type { IUpdateGroupResultAttr } from "./types";

const areMutationsValid = (
  resultMutation: ExecutionResult<IUpdateGroupResultAttr>
): boolean => {
  if (!_.isUndefined(resultMutation.data) && !_.isNull(resultMutation.data)) {
    const updateManagedSuccess: boolean = _.isUndefined(
      resultMutation.data.updateGroupManaged
    )
      ? true
      : resultMutation.data.updateGroupManaged.success;
    const updateSubscriptionSuccess: boolean = _.isUndefined(
      resultMutation.data.updateSubscription
    )
      ? true
      : resultMutation.data.updateSubscription.success;

    return updateManagedSuccess && updateSubscriptionSuccess;
  }

  return false;
};

export { areMutationsValid };
