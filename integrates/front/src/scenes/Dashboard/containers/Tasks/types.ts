import type { ApolloQueryResult } from "@apollo/client";

import type {
  IGetMeVulnerabilitiesAssigned,
  IGetUserOrganizationsGroups,
} from "scenes/Dashboard/types";

interface ITasksContent {
  meVulnerabilitiesAssigned: IGetMeVulnerabilitiesAssigned | undefined;
  userData: IGetUserOrganizationsGroups | undefined;
  refetchVulnerabilitiesAssigned: () => Promise<
    ApolloQueryResult<IGetMeVulnerabilitiesAssigned>
  >;
  setUserRole: (userRole: string | undefined) => void;
}

export type { ITasksContent };
