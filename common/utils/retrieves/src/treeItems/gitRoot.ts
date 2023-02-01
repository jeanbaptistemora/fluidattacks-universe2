import type { Command } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { TreeItem, TreeItemCollapsibleState } from "vscode";

import { getGroupGitRoots } from "../api/root";
import type { IGitRoot } from "../types";

class GitRootTreeItem extends TreeItem {
  public contextValue = "gitRoot";

  public constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly groupName: string,
    public readonly rootId: string,
    public readonly nickname: string,
    public readonly gitignore: string[],
    public readonly downloadUrl?: string,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

async function getGitRoots(groupName: string): Promise<GitRootTreeItem[]> {
  const roots: IGitRoot[] = await getGroupGitRoots(groupName);

  const toGitRoot = (root: IGitRoot): GitRootTreeItem => {
    return new GitRootTreeItem(
      root.nickname,
      TreeItemCollapsibleState.Collapsed,
      groupName,
      root.id,
      root.nickname,
      root.gitignore,
      root.downloadUrl
    );
  };

  const deps = roots
    .filter(
      (root: IGitRoot): boolean =>
        root.state === "ACTIVE" && root.downloadUrl !== undefined
    )
    .map((dep): GitRootTreeItem => toGitRoot(dep));

  return deps;
}

export { getGitRoots, GitRootTreeItem };
