import type { Command } from "vscode";
import { TreeItem, TreeItemCollapsibleState } from "vscode";

import { GET_GIT_ROOTS } from "../queries";
import type { GitRoot } from "../types";
import { getClient } from "../utils/apollo";

class GitRootTreeItem extends TreeItem {
  public contextValue = "gitRoot";

  public constructor(
    public readonly label: string,
    public readonly collapsibleState: TreeItemCollapsibleState,
    public readonly groupName: string,
    public readonly nickname: string,
    public readonly downloadUrl?: string,
    public readonly command?: Command
  ) {
    super(label, collapsibleState);
  }
}

async function getGitRoots(groupName: string): Promise<GitRootTreeItem[]> {
  const nicknames: GitRoot[] = await Promise.resolve(
    getClient()
      .query({
        query: GET_GIT_ROOTS,
        variables: { groupName },
      })
      .then((result): GitRoot[] => {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
        return result.data.group.roots;
      })
      .catch((_err): [] => {
        return [];
      })
  );
  const toGitRoot = (root: GitRoot): GitRootTreeItem => {
    return new GitRootTreeItem(
      root.nickname,
      TreeItemCollapsibleState.Collapsed,
      groupName,
      root.nickname,
      root.downloadUrl
    );
  };

  const deps = nicknames.map((dep): GitRootTreeItem => toGitRoot(dep));

  return deps;
}

export { getGitRoots, GitRootTreeItem };
