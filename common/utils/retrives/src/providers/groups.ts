/* eslint-disable fp/no-this */
import * as vscode from "vscode";

import type { GitRootTreeItem } from "./gitRoots";
import { getGitRoots } from "./gitRoots";

import { GET_GROUPS } from "../queries";
import { GroupTreeItem } from "../treeItems/group";
import type { Organization } from "../types";
import { getClient } from "../utils/apollo";

type EventGroup = GroupTreeItem | undefined | void;
type TreeItems = GitRootTreeItem[] | GroupTreeItem[];
// eslint-disable-next-line fp/no-class
class GroupsProvider implements vscode.TreeDataProvider<GroupTreeItem> {
  private readonly _onDidChangeTreeData: vscode.EventEmitter<EventGroup> =
    new vscode.EventEmitter<EventGroup>();

  public readonly onDidChangeTreeData: vscode.Event<EventGroup> =
    this._onDidChangeTreeData.event;

  public refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  public getTreeItem(element: GroupTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: GroupTreeItem): Thenable<TreeItems> {
    if (element) {
      return Promise.resolve(getGitRoots(element.label));
    }

    return Promise.resolve(this.getGroups());
  }

  private async getGroups(): Promise<GroupTreeItem[]> {
    const groups: string[] = await Promise.resolve(
      getClient()
        .query({ query: GET_GROUPS })
        .then((result: any) =>
          result.data.me.organizations
            .map((org: Organization) => org.groups.map((group) => group.name))
            .flat()
        )
        .catch((err: any): [] => {
          return [];
        })
    );

    const toGroup = (groupName: string): GroupTreeItem =>
      new GroupTreeItem(groupName, vscode.TreeItemCollapsibleState.Collapsed);

    const deps = groups.map((dep): GroupTreeItem => toGroup(dep));

    return deps;
  }
}

export { GroupsProvider };
