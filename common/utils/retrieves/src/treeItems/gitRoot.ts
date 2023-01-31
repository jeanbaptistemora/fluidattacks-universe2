import type { Command } from "vscode";
// eslint-disable-next-line import/no-unresolved
import { TreeItem, TreeItemCollapsibleState, window } from "vscode";

import { GET_GIT_ROOTS } from "../queries";
import type { IGitRoot } from "../types";
import { getClient } from "../utils/apollo";

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
  const nicknames: IGitRoot[] = await Promise.resolve(
    getClient()
      .query({
        query: GET_GIT_ROOTS,
        variables: { groupName },
      })
      .then((result): IGitRoot[] => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
        return result.data.group.roots;
      })
      .catch((_err): [] => {
        void window.showErrorMessage(String(_err));

        return [];
      })
  );

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

  const deps = nicknames
    .filter(
      (root: IGitRoot): boolean =>
        root.state === "ACTIVE" && root.downloadUrl !== undefined
    )
    .map((dep): GitRootTreeItem => toGitRoot(dep));

  return deps;
}

export { getGitRoots, GitRootTreeItem };
