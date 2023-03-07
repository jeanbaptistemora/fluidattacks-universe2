/* eslint-disable @typescript-eslint/no-invalid-void-type */
/* eslint-disable fp/no-this */

import type { Event, TreeDataProvider, TreeItem } from "vscode";
import {
  EventEmitter,
  TreeItemCollapsibleState,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import { getGroups } from "../api/groups";
import type { GitRootTreeItem } from "../treeItems/gitRoot";
import { getGitRoots } from "../treeItems/gitRoot";
import { GroupTreeItem } from "../treeItems/group";

type EventGroup = GroupTreeItem | undefined | void;
type TreeItems = GitRootTreeItem[] | GroupTreeItem[];
// eslint-disable-next-line fp/no-class
class GroupsProvider implements TreeDataProvider<GroupTreeItem> {
  private readonly onDidChangeTreeDataEventEmitter: EventEmitter<EventGroup> =
    new EventEmitter<EventGroup>();

  // eslint-disable-next-line @typescript-eslint/member-ordering
  public readonly onDidChangeTreeData: Event<EventGroup> =
    this.onDidChangeTreeDataEventEmitter.event;

  public refresh(): void {
    this.onDidChangeTreeDataEventEmitter.fire();
  }

  // eslint-disable-next-line class-methods-use-this
  public getTreeItem(element: GroupTreeItem): TreeItem {
    return element;
  }

  public getChildren(element?: GroupTreeItem): Thenable<TreeItems> {
    if (element && element.contextValue === "group") {
      return Promise.resolve(getGitRoots(element.label));
    } else if (element) {
      return Promise.resolve([]);
    }

    return Promise.resolve(this.getGroupsItems());
  }

  // eslint-disable-next-line class-methods-use-this
  private async getGroupsItems(): Promise<GroupTreeItem[]> {
    const groups: string[] = await getGroups();
    const toGroup = (groupName: string): GroupTreeItem =>
      new GroupTreeItem(groupName, TreeItemCollapsibleState.Collapsed);

    const deps = groups.map((dep): GroupTreeItem => toGroup(dep));

    return deps;
  }
}

export { GroupsProvider };
