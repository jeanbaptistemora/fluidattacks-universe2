import { TreeItem } from "vscode";
import type { Command, TreeItemCollapsibleState } from "vscode";

// eslint-disable-next-line fp/no-class
class GroupTreeItem extends TreeItem {
  public contextValue = "group";

  constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

export { GroupTreeItem };
