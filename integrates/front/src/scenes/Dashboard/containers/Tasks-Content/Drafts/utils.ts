import type { ITodoDraftAttr } from "./types";

import type { IGroups, IOrganizationGroups } from "scenes/Dashboard/types";

const formatDrafts: (
  drafts: ITodoDraftAttr[],
  organizationsGroups: IOrganizationGroups[] | undefined
) => ITodoDraftAttr[] = (
  drafts: ITodoDraftAttr[],
  organizationsGroups: IOrganizationGroups[] | undefined
): ITodoDraftAttr[] =>
  drafts.map((draft: ITodoDraftAttr): ITodoDraftAttr => {
    const organizationName: IOrganizationGroups | undefined =
      organizationsGroups === undefined
        ? undefined
        : organizationsGroups.find(
            (orgGroup: IOrganizationGroups): boolean =>
              orgGroup.groups.find(
                (group: IGroups): boolean => group.name === draft.groupName
              )?.name === draft.groupName
          );

    return {
      ...draft,
      organizationName:
        organizationName === undefined ? "" : organizationName.name,
    };
  });

export { formatDrafts };
