/* eslint-disable @typescript-eslint/no-invalid-void-type */
/* eslint-disable fp/no-this */

import type { Event, TreeDataProvider, TreeItem } from "vscode";
import { EventEmitter, TreeItemCollapsibleState } from "vscode";

import { GET_GROUPS } from "../queries";
import type { GitRootTreeItem } from "../treeItems/gitRoot";
import { getGitRoots } from "../treeItems/gitRoot";
import { GroupTreeItem } from "../treeItems/group";
import type { Organization } from "../types";
import { getClient } from "../utils/apollo";

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
    if (element) {
      return Promise.resolve(getGitRoots(element.label));
    }

    return Promise.resolve(this.getGroups());
  }

  // eslint-disable-next-line class-methods-use-this
  private async getGroups(): Promise<GroupTreeItem[]> {
    const groups: string[] = await Promise.resolve(
      getClient()
        .query({ query: GET_GROUPS })
        .then(
          (result: {
            data: {
              me: {
                organizations: Organization[];
              };
            };
          }): string[] =>
            result.data.me.organizations
              .map((org: Organization): string[] =>
                org.groups.map((group): string => group.name)
              )
              .flat()
        )
        .catch((_err): [] => {
          return [];
        })
    );
    const toGroup = (groupName: string): GroupTreeItem =>
      new GroupTreeItem(groupName, TreeItemCollapsibleState.Collapsed);

    const deps = groups.map((dep): GroupTreeItem => toGroup(dep));

    return deps;
  }
}

export { GroupsProvider };
