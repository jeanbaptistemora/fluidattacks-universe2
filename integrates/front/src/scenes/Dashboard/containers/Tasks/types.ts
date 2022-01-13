import type { IGetUserOrganizationsGroups } from "scenes/Dashboard/types";

interface ITasksContent {
  setUserRole: (userRole: string | undefined) => void;
  userData: IGetUserOrganizationsGroups | undefined;
  setTaskState: (taskState: boolean) => void;
  taskState: boolean;
}

interface IAction {
  action: string;
}
interface IGroupAction {
  groupName: string;
  actions: IAction[];
}
interface IGroupRole {
  groupName: string;
  role: string;
}

export { IAction, IGroupAction, IGroupRole, ITasksContent };
