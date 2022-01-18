import type { IGetUserOrganizationsGroups } from "scenes/Dashboard/types";

interface ITasksContent {
  userData: IGetUserOrganizationsGroups | undefined;
  setTaskState: (taskState: boolean) => void;
  setUserRole: (userRole: string | undefined) => void;
  taskState: boolean;
}

interface IAction {
  action: string;
}
interface IGroupAction {
  groupName: string;
  actions: IAction[];
}

interface IFilterTodosSet {
  tag: string;
}

export { IAction, IFilterTodosSet, IGroupAction, ITasksContent };
