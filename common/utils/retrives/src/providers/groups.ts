import * as vscode from "vscode";
import { GET_GROUPS } from "../queries";
import { getClient } from "../utils/apollo";
import { Organization } from "../types";
import { getGitRoots, GitRootTreeItem } from "./gitRoots";

type EventGroup = Group | undefined | void;
type TreeItems = Group[] | GitRootTreeItem[];
export class GroupsProvider implements vscode.TreeDataProvider<Group> {
  private _onDidChangeTreeData: vscode.EventEmitter<EventGroup> =
    new vscode.EventEmitter<EventGroup>();
  readonly onDidChangeTreeData: vscode.Event<EventGroup> =
    this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: Group): vscode.TreeItem {
    return element;
  }

  getChildren(element?: Group): Thenable<TreeItems> {
    if (element) {
      return Promise.resolve(getGitRoots(element.label));
    } else {
      return Promise.resolve(this.getGroups());
    }
  }

  private async getGroups(): Promise<Group[]> {
    let groups: string[] = await Promise.resolve(
      getClient()
        .query({ query: GET_GROUPS })
        .then((result) => {
          return result.data.me.organizations
            .map((org: Organization) => {
              return org.groups.map((group) => group.name);
            })
            .flat();
        })
        .catch((err) => {
          console.log(err);
          return [];
        })
    );
    const toGroup = (groupName: string): Group => {
      return new Group(groupName, vscode.TreeItemCollapsibleState.Collapsed);
    };

    const deps = groups.map((dep) => toGroup(dep));
    return deps;
  }
}

export class Group extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly command?: vscode.Command
  ) {
    super(label, collapsibleState);
  }

  contextValue = "group";
}
