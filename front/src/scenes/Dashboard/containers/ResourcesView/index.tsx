/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { NetworkStatus } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidFileName, isValidFileSize } from "../../../../utils/validations";
import { addEnvironmentsModal as AddEnvironmentsModal } from "../../components/AddEnvironmentsModal/index";
import { AddFilesModal } from "../../components/AddFilesModal/index";
import { addRepositoriesModal as AddRepositoriesModal } from "../../components/AddRepositoriesModal/index";
import { addTagsModal as AddTagsModal } from "../../components/AddTagsModal/index";
import { fileOptionsModal as FileOptionsModal } from "../../components/FileOptionsModal/index";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import { ADD_ENVS_MUTATION, ADD_REPOS_MUTATION, ADD_TAGS_MUTATION, GET_ENVIRONMENTS, GET_REPOSITORIES,
  GET_TAGS, REMOVE_ENV_MUTATION, REMOVE_REPO_MUTATION, REMOVE_TAG_MUTATION } from "./queries";
import { IAddEnvAttr, IAddReposAttr, IAddTagsAttr, IEnvironmentsAttr, IProjectTagsAttr, IRemoveEnvAttr, IRemoveRepoAttr,
  IRemoveTagsAttr, IRepositoriesAttr, IResourcesAttr, IResourcesViewBaseProps, IResourcesViewDispatchProps,
  IResourcesViewProps, IResourcesViewStateProps } from "./types";

const enhance: InferableComponentEnhancer<{}> = lifecycle<IResourcesViewProps, {}>({
  componentDidMount(): void {
    mixpanel.track(
      "ProjectResources",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    this.props.onLoad();
  },
});

const getSelectedRow: ((tableId: string) => HTMLTableRowElement | undefined) =
  (tableId: string): HTMLTableRowElement | undefined => {
    const selectedQry: NodeListOf<Element> = document.querySelectorAll(`#${tableId} tr input:checked`);
    const selectedRow: HTMLTableRowElement | null | undefined =
      _.isEmpty(selectedQry) ? undefined : selectedQry[0].closest("tr");

    return selectedRow === undefined || selectedRow === null ? undefined : selectedRow;
  };

const handleSaveFiles: ((files: IResourcesViewProps["files"], props: IResourcesViewProps) => void) =
  (files: IResourcesViewProps["files"], props: IResourcesViewProps): void => {
    const selected: FileList | null = (document.querySelector("#file") as HTMLInputElement).files;
    if (_.isNil(selected) || selected.length === 0) {
      msgError(translate.t("proj_alerts.no_file_selected"));
      throw new Error();
    } else {
      files[0].fileName = selected[0].name;
    }
    let fileSize: number; fileSize = 100;
    if (isValidFileName(files[0].fileName)) {
      if (isValidFileSize(selected[0], fileSize)) {
        mixpanel.track(
          "AddProjectFiles",
          {
            Organization: (window as Window & { userOrganization: string }).userOrganization,
            User: (window as Window & { userName: string }).userName,
          });
        let containsRepeated: boolean;
        containsRepeated = files.filter(
          (newItem: IResourcesViewProps["files"][0]) => _.findIndex(
            props.files,
            (currentItem: IResourcesViewProps["files"][0]) =>
              currentItem.fileName === newItem.fileName,
          ) > -1).length > 0;
        if (containsRepeated) {
          msgError(translate.t("search_findings.tab_resources.repeated_item"));
        } else {
          props.onSaveFiles(files);
        }
      }
    } else {
      msgError(translate.t("search_findings.tab_resources.invalid_chars"));
    }
  };

const containsRepeatedTags: (
  (currTags: IProjectTagsAttr["project"]["tags"], tags: IProjectTagsAttr["project"]["tags"]) => boolean) =
  (currTags: IProjectTagsAttr["project"]["tags"], tags: IProjectTagsAttr["project"]["tags"]): boolean => {
    let containsRepeated: boolean;
    containsRepeated = currTags.filter(
      (newItem: IProjectTagsAttr["project"]["tags"][0]) => _.findIndex(
        tags,
        (currentItem: IProjectTagsAttr["project"]["tags"][0]) =>
          currentItem === newItem,
      ) > -1).length > 0;

    return containsRepeated;
  };

const containsRepeatedRepos: ((currRepo: IRepositoriesAttr[], repos: IRepositoriesAttr[]) => boolean) =
  (currRepo: IRepositoriesAttr[], repos: IRepositoriesAttr[]): boolean => {
    let containsRepeated: boolean;
    containsRepeated = currRepo.filter(
      (newItem: IRepositoriesAttr[][0]) => _.findIndex(
        repos,
        (currentItem: IRepositoriesAttr[][0]) =>
          currentItem.urlRepo === newItem.urlRepo && currentItem.branch === newItem.branch,
      ) > -1).length > 0;

    return containsRepeated;
  };

const containsRepeatedEnvs: ((currEnv: IEnvironmentsAttr[], environments: IEnvironmentsAttr[]) => boolean) =
  (currEnv: IEnvironmentsAttr[], environments: IEnvironmentsAttr[]): boolean => {
    let containsRepeated: boolean;
    containsRepeated = currEnv.filter(
      (newItem: IEnvironmentsAttr[][0]) => _.findIndex(
        environments,
        (currentItem: IEnvironmentsAttr[][0]) =>
          currentItem.urlEnv === newItem.urlEnv,
      ) > -1).length > 0;

    return containsRepeated;
  };

const renderTagsView: ((props: IResourcesViewProps) => JSX.Element) = (props: IResourcesViewProps): JSX.Element => {
  const handleOpenTagsModal: (() => void) = (): void => { props.onOpenTagsModal(); };
  const handleCloseTagsModal: (() => void) = (): void => { props.onCloseTagsModal(); };
  const projectName: string = props.match.params.projectName;

  const handleQryResult: ((qrResult: IProjectTagsAttr) => void) = (qrResult: IProjectTagsAttr): void => {
    mixpanel.track(
      "ProjectTags",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    hidePreloader();
  };

  return (
    <Query
      query={GET_TAGS}
      variables={{ projectName }}
      notifyOnNetworkStatusChange={true}
      onCompleted={handleQryResult}
    >
      {
        ({loading, error, data, refetch, networkStatus}: QueryResult<IProjectTagsAttr>): React.ReactNode => {
          const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
          if (loading || isRefetching) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting tags", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data) && !_.isEmpty(data.project.subscription) && _.isEmpty(data.project.deletionDate)) {
            const tagsDataset: Array<{ tagName: string }> = data.project.tags.map(
              (tagName: string) => ({ tagName }));

            const handleMtRemoveTagRes: ((mtResult: IRemoveTagsAttr) => void) = (mtResult: IRemoveTagsAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.removeTag.success) {
                  hidePreloader();
                  refetch()
                      .catch();
                  mixpanel.track(
                    "RemoveProjectTags",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success_remove"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtAddTagRes: ((mtResult: IAddTagsAttr) => void) = (mtResult: IAddTagsAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.addTags.success) {
                  refetch()
                    .catch();
                  handleCloseTagsModal();
                  hidePreloader();
                  mixpanel.track(
                    "AddProjectTags",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            return (
              <React.Fragment>
                <hr/>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTable
                      dataset={tagsDataset}
                      enableRowSelection={true}
                      exportCsv={false}
                      search={false}
                      headers={[
                        {
                          dataField: "tagName",
                          header: translate.t("search_findings.tab_resources.tags_title"),
                          isDate: false,
                          isStatus: false,
                        },
                      ]}
                      id="tblTags"
                      pageSize={15}
                      title={translate.t("search_findings.tab_resources.tags_title")}
                      selectionMode="radio"
                    />
                  </Col>
                  <Col md={12}>
                    <br />
                    <Col mdOffset={4} md={2} sm={6}>
                      <Button id="addTag" block={true} bsStyle="primary" onClick={handleOpenTagsModal}>
                        <Glyphicon glyph="plus" />&nbsp;
                        {translate.t("search_findings.tab_resources.add_repository")}
                      </Button>
                    </Col>
                    <Mutation mutation={REMOVE_TAG_MUTATION} onCompleted={handleMtRemoveTagRes}>
                      { (removeTag: MutationFn<IRemoveTagsAttr, {projectName: string; tagToRemove: string}>,
                         mutationRes: MutationResult): React.ReactNode => {
                          if (mutationRes.loading) {
                            showPreloader();
                          }
                          if (!_.isUndefined(mutationRes.error)) {
                            hidePreloader();
                            handleGraphQLErrors("An error occurred removing tags", mutationRes.error);

                            return <React.Fragment/>;
                          }

                          const handleRemoveTag: (() => void) = (): void => {
                            const selectedQry: NodeListOf<Element> = document.querySelectorAll(
                              "#tblTags tr input:checked");
                            if (selectedQry.length > 0) {
                              if (selectedQry[0].closest("tr") !== null) {
                                const selectedRow: Element = selectedQry[0].closest("tr") as Element;
                                const tag: string | null = selectedRow.children[1].textContent;
                                removeTag({
                                  variables: { projectName: props.match.params.projectName, tagToRemove: String(tag)},
                                })
                                  .catch();
                              } else {
                                msgError(translate.t("proj_alerts.error_textsad"));
                                rollbar.error("An error occurred removing tags");
                              }
                            } else {
                              msgError(translate.t("search_findings.tab_resources.no_selection"));
                            }
                          };

                          return (
                            <Col md={2} sm={6}>
                              <Button
                                id="removeTag"
                                block={true}
                                bsStyle="primary"
                                onClick={handleRemoveTag}
                              >
                                <Glyphicon glyph="minus" />&nbsp;
                                {translate.t("search_findings.tab_resources.remove_repository")}
                              </Button>
                            </Col>
                          );
                      }}
                    </Mutation>
                  </Col>
                  <Col md={12}>
                    <br />
                    <label style={{fontSize: "15px"}}>
                      <b>{translate.t("search_findings.tab_resources.total_tags")}</b>
                      {tagsDataset.length}
                    </label>
                  </Col>
                </Row>
                <Mutation mutation={ADD_TAGS_MUTATION} onCompleted={handleMtAddTagRes}>
                  { (addTags: MutationFn<IAddTagsAttr, {projectName: string; tagsData: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }
                      if (!_.isUndefined(mutationRes.error)) {
                        hidePreloader();
                        handleGraphQLErrors("An error occurred adding tags", mutationRes.error);

                        return <React.Fragment/>;
                      }

                      const handleSubmitTag: ((values: { tags: string[] }) => void) =
                        (values: { tags: string[] }): void => {
                          if (containsRepeatedTags(values.tags, data.project.tags)) {
                            msgError(translate.t("search_findings.tab_resources.repeated_item"));
                          } else {
                            addTags({
                              variables: { projectName: props.match.params.projectName,
                                           tagsData: JSON.stringify(values.tags)},
                              },
                            )
                              .catch();
                          }
                        };

                      return (
                        <AddTagsModal
                          isOpen={props.tagsModal.open}
                          onClose={handleCloseTagsModal}
                          onSubmit={handleSubmitTag}
                        />
                      );
                  }}
                </Mutation>
              </React.Fragment>
            );
          }
        }}
    </Query>
  );
};

const renderRespositories: ((props: IResourcesViewProps) => JSX.Element) =
  (props: IResourcesViewProps): JSX.Element => {
    const handleAddRepoClick: (() => void) = (): void => { props.onOpenReposModal(); };
    const handleCloseReposModalClick: (() => void) = (): void => { props.onCloseReposModal(); };
    const projectName: string = props.match.params.projectName;

    return (
      <Query query={GET_REPOSITORIES} variables={{ projectName }} notifyOnNetworkStatusChange={true}>
      {
        ({loading, error, data, refetch, networkStatus}: QueryResult<IResourcesAttr>): React.ReactNode => {
          const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
          if (loading || isRefetching) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting repositories", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            hidePreloader();
            const repoDataset: IRepositoriesAttr[] = JSON.parse(data.resources.repositories);

            const handleMtRemoveRepoRes: ((mtResult: IRemoveRepoAttr) => void) = (mtResult: IRemoveRepoAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.removeRepositories.success) {
                  hidePreloader();
                  refetch()
                      .catch();
                  mixpanel.track(
                    "RemoveProjectRepo",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success_remove"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtAddReposRes: ((mtResult: IAddReposAttr) => void) = (mtResult: IAddReposAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.addRepositories.success) {
                  refetch()
                    .catch();
                  handleCloseReposModalClick();
                  hidePreloader();
                  mixpanel.track(
                    "AddProjectRepo",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            return (
              <React.Fragment>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTable
                      dataset={repoDataset}
                      selectionMode="radio"
                      enableRowSelection={true}
                      exportCsv={true}
                      search={true}
                      headers={[
                        {
                          dataField: "protocol",
                          header: translate.t("search_findings.repositories_table.protocol"),
                          isDate: false,
                          isStatus: false,
                          width: "20%",
                          wrapped: true,
                        },
                        {
                          dataField: "urlRepo",
                          header: translate.t("search_findings.repositories_table.repository"),
                          isDate: false,
                          isStatus: false,
                          width: "60%",
                          wrapped: true,
                        },
                        {
                          dataField: "branch",
                          header: translate.t("search_findings.repositories_table.branch"),
                          isDate: false,
                          isStatus: false,
                          width: "20%",
                          wrapped: true,
                        },
                      ]}
                      id="tblRepositories"
                      pageSize={15}
                      title={translate.t("search_findings.tab_resources.repositories_title")}
                    />
                  </Col>
                  <Col md={12}>
                    <br />
                    <Col mdOffset={4} md={2} sm={6}>
                      <Button
                        id="addRepository"
                        block={true}
                        bsStyle="primary"
                        onClick={handleAddRepoClick}
                      >
                        <Glyphicon glyph="plus"/>&nbsp;
                        {translate.t("search_findings.tab_resources.add_repository")}
                      </Button>
                    </Col>
                    <Mutation mutation={REMOVE_REPO_MUTATION} onCompleted={handleMtRemoveRepoRes}>
                      { (removeRepositories: MutationFn<IRemoveRepoAttr, {projectName: string; repoData: string}>,
                         mutationRes: MutationResult): React.ReactNode => {
                          if (mutationRes.loading) {
                            showPreloader();
                          }
                          if (!_.isUndefined(mutationRes.error)) {
                            hidePreloader();
                            handleGraphQLErrors("An error occurred removing repositories", mutationRes.error);

                            return <React.Fragment/>;
                          }

                          const handleRemoveRepo: (() => void) = (): void => {
                            const selectedRow: HTMLTableRowElement | undefined = getSelectedRow("tblRepositories");
                            if (selectedRow === undefined) {
                              msgError(translate.t("search_findings.tab_resources.no_selection"));
                            } else {
                              const protocol: string | null = selectedRow.children[1].textContent;
                              const repository: string | null = selectedRow.children[2].textContent;
                              const branch: string | null = selectedRow.children[3].textContent;
                              const repoRemoved: {[value: string]: string | null} = {
                                branch,
                                protocol,
                                urlRepo: repository,
                              };
                              removeRepositories({ variables: { projectName, repoData: JSON.stringify(repoRemoved)} })
                                .catch();
                            }
                          };

                          return(
                            <Col md={2} sm={6}>
                              <Button
                                id="removeRepository"
                                block={true}
                                bsStyle="primary"
                                onClick={handleRemoveRepo}
                              >
                                <Glyphicon glyph="minus"/>&nbsp;
                                {translate.t("search_findings.tab_resources.remove_repository")}
                              </Button>
                            </Col>
                          );
                        }}
                    </Mutation>
                  </Col>
                  <Col md={12}>
                    <br />
                    <label style={{fontSize: "15px"}}>
                      <b>{translate.t("search_findings.tab_resources.total_repos")}</b>
                      {repoDataset.length}
                    </label>
                  </Col>
                </Row>
                <Mutation mutation={ADD_REPOS_MUTATION} onCompleted={handleMtAddReposRes}>
                  { (addRepositories: MutationFn<IAddReposAttr, {projectName: string; repoData: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }
                      if (!_.isUndefined(mutationRes.error)) {
                        hidePreloader();
                        handleGraphQLErrors("An error occurred adding repositories", mutationRes.error);

                        return <React.Fragment/>;
                      }

                      const handleAddRepo: ((values: { resources: IRepositoriesAttr[] }) => void) =
                        (values: { resources: IRepositoriesAttr[] }): void => {
                          if (containsRepeatedRepos(values.resources, repoDataset)) {
                            msgError(translate.t("search_findings.tab_resources.repeated_item"));
                          } else {
                            addRepositories({
                              variables: { projectName, repoData: JSON.stringify(values.resources)},
                              },
                            )
                              .catch();
                          }
                        };

                      return (
                        <AddRepositoriesModal
                          isOpen={props.reposModal.open}
                          onClose={handleCloseReposModalClick}
                          onSubmit={handleAddRepo}
                        />
                      );
                  }}
                </Mutation>
              </React.Fragment>
            );
          }
        }}
      </Query>
    );
  };

const renderEnvironments: ((props: IResourcesViewProps) => JSX.Element) =
  (props: IResourcesViewProps): JSX.Element => {
    const handleAddEnvClick: (() => void) = (): void => { props.onOpenEnvsModal(); };
    const handleCloseEnvModalClick: (() => void) = (): void => { props.onCloseEnvsModal(); };
    const projectName: string = props.match.params.projectName;

    return (
      <Query query={GET_ENVIRONMENTS} variables={{ projectName }} notifyOnNetworkStatusChange={true}>
      {
        ({loading, error, data, refetch, networkStatus}: QueryResult<IResourcesAttr>): React.ReactNode => {
          const isRefetching: boolean = networkStatus === NetworkStatus.refetch;
          if (loading || isRefetching) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting environments", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            hidePreloader();
            const envDataset: IEnvironmentsAttr[] = JSON.parse(data.resources.environments);

            const handleMtRemoveEnvRes: ((mtResult: IRemoveEnvAttr) => void) = (mtResult: IRemoveEnvAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.removeEnvironments.success) {
                  hidePreloader();
                  refetch()
                      .catch();
                  mixpanel.track(
                    "RemoveProjectEnv",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success_remove"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtAddEnvsRes: ((mtResult: IAddEnvAttr) => void) = (mtResult: IAddEnvAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.addEnvironments.success) {
                  refetch()
                    .catch();
                  handleCloseEnvModalClick();
                  hidePreloader();
                  mixpanel.track(
                    "AddProjectEnv",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            return (
              <React.Fragment>
                <hr/>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTable
                      dataset={envDataset}
                      enableRowSelection={true}
                      exportCsv={true}
                      search={true}
                      selectionMode="radio"
                      headers={[
                        {
                          dataField: "urlEnv",
                          header: translate.t("search_findings.environment_table.environment"),
                          isDate: false,
                          isStatus: false,
                          wrapped: true,
                        },
                      ]}
                      id="tblEnvironments"
                      pageSize={15}
                      title={translate.t("search_findings.tab_resources.environments_title")}
                    />
                  </Col>
                  <Col md={12}>
                    <br />
                    <Col mdOffset={4} md={2} sm={6}>
                      <Button
                        id="addEnvironment"
                        block={true}
                        bsStyle="primary"
                        onClick={handleAddEnvClick}
                      >
                        <Glyphicon glyph="plus"/>&nbsp;
                        {translate.t("search_findings.tab_resources.add_repository")}
                      </Button>
                    </Col>
                    <Mutation mutation={REMOVE_ENV_MUTATION} onCompleted={handleMtRemoveEnvRes}>
                      { (removeEnvironments: MutationFn<IRemoveEnvAttr, {envData: string; projectName: string}>,
                         mutationRes: MutationResult): React.ReactNode => {
                          if (mutationRes.loading) {
                            showPreloader();
                          }
                          if (!_.isUndefined(mutationRes.error)) {
                            hidePreloader();
                            handleGraphQLErrors("An error occurred removing environments", mutationRes.error);

                            return <React.Fragment/>;
                          }

                          const handleRemoveEnv: (() => void) = (): void => {
                            const selectedRow: HTMLTableRowElement | undefined = getSelectedRow("tblEnvironments");
                            if (selectedRow === undefined) {
                              msgError(translate.t("search_findings.tab_resources.no_selection"));
                            } else {
                              const env: string | null = selectedRow.children[1].textContent;
                              const envRemoved: {[value: string]: string | null} = {
                                urlEnv: env,
                              };
                              removeEnvironments({ variables: { projectName, envData: JSON.stringify(envRemoved)} })
                                .catch();
                            }
                          };

                          return (
                            <Col md={2} sm={6}>
                              <Button
                                id="removeEnvironment"
                                block={true}
                                bsStyle="primary"
                                onClick={handleRemoveEnv}
                              >
                                <Glyphicon glyph="minus"/>&nbsp;
                                {translate.t("search_findings.tab_resources.remove_repository")}
                              </Button>
                            </Col>
                          );
                        }}
                    </Mutation>
                  </Col>
                  <Col md={12}>
                    <br />
                    <label style={{fontSize: "15px"}}>
                      <b>{translate.t("search_findings.tab_resources.total_envs")}</b>
                      {envDataset.length}
                    </label>
                  </Col>
                </Row>
                <Mutation mutation={ADD_ENVS_MUTATION} onCompleted={handleMtAddEnvsRes}>
                  { (addEnvironments: MutationFn<IAddEnvAttr, {envData: string; projectName: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }
                      if (!_.isUndefined(mutationRes.error)) {
                        hidePreloader();
                        handleGraphQLErrors("An error occurred adding environments", mutationRes.error);

                        return <React.Fragment/>;
                      }

                      const handleAddEnv: ((values: { resources: IEnvironmentsAttr[] }) => void) =
                        (values: { resources: IEnvironmentsAttr[] }): void => {
                          if (containsRepeatedEnvs(values.resources, envDataset)) {
                            msgError(translate.t("search_findings.tab_resources.repeated_item"));
                          } else {
                            addEnvironments({
                              variables: { projectName, envData: JSON.stringify(values.resources)},
                              },
                            )
                              .catch();
                          }
                        };

                      return (
                        <AddEnvironmentsModal
                          isOpen={props.envModal.open}
                          onClose={handleCloseEnvModalClick}
                          onSubmit={handleAddEnv}
                        />
                      );
                    }}
                </Mutation>
              </React.Fragment>
            );
          }
        }}
      </Query>
    );
  };

const renderFiles: ((props: IResourcesViewProps) => JSX.Element) =
  (props: IResourcesViewProps): JSX.Element => {
    const handleAddFileClick: (() => void) = (): void => { props.onOpenFilesModal(); };
    const handleCloseFilesModalClick: (() => void) = (): void => { props.onCloseFilesModal(); };
    const handleCloseOptionsModalClick: (() => void) = (): void => { props.onCloseOptionsModal(); };
    const handleDeleteFileClick: (() => void) = (): void => {
      mixpanel.track(
        "RemoveProjectFiles",
        {
          Organization: (window as Window & { userOrganization: string }).userOrganization,
          User: (window as Window & { userName: string }).userName,
        });
      props.onDeleteFile(props.optionsModal.rowInfo.fileName);
    };
    const handleDownloadFileClick: (() => void) = (): void => {
      props.onDownloadFile(props.optionsModal.rowInfo.fileName);
    };
    const handleFileRowClick: ((row: string) => void) = (row: string): void => { props.onOpenOptionsModal(row); };

    const handleAddFile: ((values: IResourcesViewProps["files"][0]) => void) = (
      values: IResourcesViewProps["files"][0]): void => {
      handleSaveFiles([{ description: values.description, fileName: "", uploadDate: "" }], props);
    };

    return (
      <React.Fragment>
        <hr/>
        <Row>
          <Col md={12} sm={12}>
            <DataTable
              dataset={props.files}
              onClickRow={handleFileRowClick}
              selectionMode="radio"
              enableRowSelection={false}
              exportCsv={false}
              search={true}
              headers={[
                {
                  dataField: "fileName",
                  header: translate.t("search_findings.files_table.file"),
                  isDate: false,
                  isStatus: false,
                  width: "25%",
                  wrapped: true,
                },
                {
                  dataField: "description",
                  header: translate.t("search_findings.files_table.description"),
                  isDate: false,
                  isStatus: false,
                  width: "50%",
                  wrapped: true,
                },
                {
                  dataField: "uploadDate",
                  header: translate.t("search_findings.files_table.upload_date"),
                  isDate: false,
                  isStatus: false,
                  width: "25%",
                  wrapped: true,
                },
              ]}
              id="tblFiles"
              pageSize={15}
              title={translate.t("search_findings.tab_resources.files_title")}
            />
          </Col>
          <Col md={12}>
            <br />
            <Col mdOffset={5} md={2} sm={6}>
              <Button
                id="addFile"
                block={true}
                bsStyle="primary"
                onClick={handleAddFileClick}
              >
                <Glyphicon glyph="plus"/>&nbsp;
                {translate.t("search_findings.tab_resources.add_repository")}
              </Button>
            </Col>
          </Col>
          <Col md={12}>
            <br />
            <label style={{fontSize: "15px"}}>
              <b>{translate.t("search_findings.tab_resources.total_files")}</b>
              {props.files.length}
            </label>
          </Col>
        </Row>
        <AddFilesModal
          isOpen={props.filesModal.open}
          onClose={handleCloseFilesModalClick}
          onSubmit={handleAddFile}
          showUploadProgress={props.showUploadProgress}
          uploadProgress={props.uploadProgress}
        />
        <FileOptionsModal
          fileName={props.optionsModal.rowInfo.fileName}
          isOpen={props.optionsModal.open}
          onClose={handleCloseOptionsModalClick}
          onSubmit={handleAddFile}
          onDelete={handleDeleteFileClick}
          onDownload={handleDownloadFileClick}
        />
      </React.Fragment>
    );
};

const projectResourcesView: React.FunctionComponent<IResourcesViewProps> =
  (props: IResourcesViewProps): JSX.Element =>
  (
  <React.StrictMode>
    <div id="resources" className="tab-pane cont active">
      {renderRespositories(props)}
      {renderEnvironments(props)}
      {renderFiles(props)}
      {renderTagsView(props)}
    </div>
  </React.StrictMode>
  );

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IResourcesViewStateProps, IResourcesViewBaseProps, IState> =
  (state: IState): IResourcesViewStateProps => ({
    envModal: state.dashboard.resources.envModal,
    files: state.dashboard.resources.files,
    filesModal: state.dashboard.resources.filesModal,
    optionsModal: state.dashboard.resources.optionsModal,
    reposModal: state.dashboard.resources.reposModal,
    showUploadProgress: state.dashboard.resources.showUploadProgress,
    tagsModal: state.dashboard.tags.tagsModal,
    uploadProgress: state.dashboard.resources.uploadProgress,
  });

const mapDispatchToProps: MapDispatchToProps<IResourcesViewDispatchProps, IResourcesViewBaseProps> =
  (dispatch: actions.ThunkDispatcher, ownProps: IResourcesViewBaseProps): IResourcesViewDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onCloseEnvsModal: (): void => { dispatch(actions.closeAddEnvModal()); },
      onCloseFilesModal: (): void => { dispatch(actions.closeAddFilesModal()); },
      onCloseOptionsModal: (): void => { dispatch(actions.closeOptionsModal()); },
      onCloseReposModal: (): void => { dispatch(actions.closeAddRepoModal()); },
      onCloseTagsModal: (): void => { dispatch(actions.closeTagsModal()); },
      onDeleteFile: (fileName: string): void => { dispatch(actions.deleteFile(projectName, fileName)); },
      onDownloadFile: (fileName: string): void => { dispatch(actions.downloadFile(projectName, fileName)); },
      onLoad: (): void => {
        dispatch(actions.loadResources(projectName));
      },
      onOpenEnvsModal: (): void => { dispatch(actions.openAddEnvModal()); },
      onOpenFilesModal: (): void => { dispatch(actions.openAddFilesModal()); },
      onOpenOptionsModal: (row: string): void => { dispatch(actions.openOptionsModal(row)); },
      onOpenReposModal: (): void => { dispatch(actions.openAddRepoModal()); },
      onOpenTagsModal: (): void => { dispatch(actions.openTagsModal()); },
      onSaveFiles: (files: IResourcesViewProps["files"]): void => { dispatch(actions.saveFiles(projectName, files)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectResourcesView));
