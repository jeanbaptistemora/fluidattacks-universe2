// eslint-disable-next-line import/no-unresolved
import { TreeItem } from "vscode";
import type { Command, TreeItemCollapsibleState } from "vscode";

class GroupTreeItem extends TreeItem {
  public contextValue = "group";

  public constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

export { GroupTreeItem };
