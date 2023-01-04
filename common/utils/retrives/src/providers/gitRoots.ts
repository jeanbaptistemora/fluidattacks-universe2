import * as vscode from "vscode";
import { GET_GIT_ROOTS } from "../queries";
import { getClient } from "../utils/apollo";
import { GitRoot } from "../types";

async function getGitRoots(groupName: string): Promise<GitRootTreeItem[]> {
  let nicknames: GitRoot[] = await Promise.resolve(
    getClient()
      .query({
        query: GET_GIT_ROOTS,
        variables: { groupName: groupName },
      })
      .then((result) => {
        return result.data.group.roots;
      })
      .catch((err) => {
        console.log(err);
        return [];
      })
  );
  const toGitRoot = (root: GitRoot): GitRootTreeItem => {
    return new GitRootTreeItem(
      root.nickname,
      vscode.TreeItemCollapsibleState.Collapsed,
      root.downloadUrl
    );
  };

  const deps = nicknames.map((dep) => toGitRoot(dep));
  return deps;
}

export class GitRootTreeItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly downloadUrl?: string,
    public readonly command?: vscode.Command
  ) {
    super(label, collapsibleState);
  }

  contextValue = "gitRoot";
}

export { getGitRoots };
