import { RouteComponentProps } from "react-router";
import { IDashboardState } from "../../reducer";

export interface IProjectTagsAttr {
  project: {
    deletionDate: string;
    name: string;
    subscription: string;
    tags: string[];
  };
}

export interface IRemoveTagsAttr {
  removeTag: {
    project: {
      deletionDate: string;
      name: string;
      subscription: string;
      tags: string[];
    };
    success: boolean;
  };
}

export interface IAddTagsAttr {
  addTags: {
    project: {
      deletionDate: string;
      name: string;
      subscription: string;
      tags: string[];
    };
    success: boolean;
  };
}

export type IResourcesViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export type IResourcesViewStateProps = IDashboardState["resources"] & IDashboardState["tags"];

export interface IResourcesViewDispatchProps {
  onCloseEnvsModal(): void;
  onCloseFilesModal(): void;
  onCloseOptionsModal(): void;
  onCloseReposModal(): void;
  onCloseTagsModal(): void;
  onDeleteFile(fileName: string): void;
  onDownloadFile(fileName: string): void;
  onLoad(): void;
  onOpenEnvsModal(): void;
  onOpenFilesModal(): void;
  onOpenOptionsModal(row: string): void;
  onOpenReposModal(): void;
  onOpenTagsModal(): void;
  onRemoveEnv(environment: string): void;
  onRemoveRepo(repoData: {[value: string]: string | null}): void;
  onSaveEnvs(environments: IResourcesViewStateProps["environments"]): void;
  onSaveFiles(files: IResourcesViewStateProps["files"]): void;
  onSaveRepos(resources: IResourcesViewStateProps["repositories"]): void;
}

export type IResourcesViewProps = IResourcesViewBaseProps & (IResourcesViewStateProps & IResourcesViewDispatchProps);
