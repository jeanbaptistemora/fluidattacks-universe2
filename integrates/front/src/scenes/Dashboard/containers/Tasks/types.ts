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

interface IAction {
  action: string;
}
interface IGroupAction {
  groupName: string;
  actions: IAction[];
}

interface IFilterTodosSet {
  reportDateRange?: { max: string; min: string };
  tag: string;
  treatment: string;
  treatmentCurrentStatus: string;
  verification?: string;
}

export { IAction, IFilterTodosSet, IGroupAction, ITasksContent };
