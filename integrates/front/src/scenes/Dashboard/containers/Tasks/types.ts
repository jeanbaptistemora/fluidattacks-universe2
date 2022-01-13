import type { IGetUserOrganizationsGroups } from "scenes/Dashboard/types";

interface ITasksContent {
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

export { IAction, IGroupAction, ITasksContent };
