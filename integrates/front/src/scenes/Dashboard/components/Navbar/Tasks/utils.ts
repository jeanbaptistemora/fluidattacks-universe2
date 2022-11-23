import _ from "lodash";

import type { IGetVulnsGroups } from "scenes/Dashboard/types";

const mergedAssigned = (
  currentAssigned: IGetVulnsGroups[],
  newAssigned: IGetVulnsGroups[]
): IGetVulnsGroups[] => {
  const newGroupAssigned: string[] = newAssigned.map(
    (groupAssigned: IGetVulnsGroups): string => groupAssigned.group.name
  );
  const filteredAssigned: IGetVulnsGroups[] = currentAssigned.filter(
    (groupAssigned: IGetVulnsGroups): boolean =>
      !_.includes(newGroupAssigned, groupAssigned.group.name)
  );

  return [...filteredAssigned, ...newAssigned];
};

export { mergedAssigned };
