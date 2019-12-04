/* tslint:disable:jsx-no-multiline-js max-file-line-count
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 * MAX-FILE-LINE-COUNT: this file exceeds by 22 the maximum of 1000 lines
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
import { ConfirmDialog } from "../../../../components/ConfirmDialog/index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidFileName, isValidFileSize } from "../../../../utils/validations";
import { openConfirmDialog } from "../../actions";
import { addEnvironmentsModal as AddEnvironmentsModal } from "../../components/AddEnvironmentsModal/index";
import { AddFilesModal } from "../../components/AddFilesModal/index";
import { addRepositoriesModal as AddRepositoriesModal } from "../../components/AddRepositoriesModal/index";
import { addTagsModal as AddTagsModal } from "../../components/AddTagsModal/index";
import { fileOptionsModal as FileOptionsModal } from "../../components/FileOptionsModal/index";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import { ADD_RESOURCE_MUTATION, ADD_TAGS_MUTATION, GET_ENVIRONMENTS, GET_REPOSITORIES,
  GET_TAGS, REMOVE_TAG_MUTATION, UPDATE_RESOURCE_MUTATION } from "./queries";
import { IAddEnvAttr, IAddReposAttr, IAddTagsAttr, IEnvironmentsAttr, IProjectTagsAttr,
  IRemoveTagsAttr, IRepositoriesAttr, IResourcesAttr, IResourcesViewBaseProps, IResourcesViewDispatchProps,
  IResourcesViewProps, IResourcesViewStateProps, IUpdateEnvAttr, IUpdateRepoAttr } from "./types";

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

const getSwitchButtonState: ((button: Element) => boolean) = (button: Element): boolean =>
  button.classList.contains("on");

const changeSwitchButtonState: ((button: Element) => void) = (button: Element): void => {
  if (!getSwitchButtonState(button)) {
    button.classList.replace("off", "on");
    button.classList.replace("btn-light", "btn-danger");
  } else {
    button.classList.replace("on", "off");
    button.classList.replace("btn-danger", "btn-light");
  }
};

const findSwitchButton: ((rowId: string, resType: string) => Element | undefined) =
  (rowId: string, resType: string): Element | undefined => {
  const resTypeInt: number = resType === "repository" ? 2 : 1;
  const statesHTMLCol: HTMLCollectionOf<Element> = document.getElementsByClassName("switch");
  const states: Element[] = Array.prototype.slice.call(statesHTMLCol);
  for (const state of states) {
    const button: Element = state;
    let id: HTMLElement | null = button.parentElement;
    for (let c: number = 0; c < resTypeInt; c++) {
      if (id !== null) {
        id = id.previousSibling as HTMLElement;
      }
    }
    if (id !== null && id.innerHTML === rowId) {
      return button;
    }
  }

  return undefined;
};

let currUserRole: string = "";

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
                      enableRowSelection={currUserRole === "customer"}
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
                      {currUserRole === "customer" ?
                      <Button
                        id="addTag"
                        block={true}
                        bsStyle="primary"
                        onClick={handleOpenTagsModal}
                      >
                        <Glyphicon glyph="plus" />&nbsp;
                        {translate.t("search_findings.tab_resources.add_repository")}
                      </Button> : undefined}
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
                              {currUserRole === "customer" ?
                              <Button
                                id="removeTag"
                                block={true}
                                bsStyle="primary"
                                onClick={handleRemoveTag}
                              >
                                <Glyphicon glyph="minus" />&nbsp;
                                {translate.t("search_findings.tab_resources.remove_repository")}
                              </Button> : undefined}
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

const renderRepositories: ((props: IResourcesViewProps) => JSX.Element) =
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
            if (data.me !== undefined) {
              currUserRole = data.me.role;
            }
            let repos: IRepositoriesAttr[] = JSON.parse(data.resources.repositories);
            repos = repos.map((repo: IRepositoriesAttr) => {
              repo.state = "ACTIVE";
              if ("historic_state" in repo) {
                repo.state = repo.historic_state[repo.historic_state.length - 1].state;
              }
              repo.state = repo.state.charAt(0) + repo.state.slice(1)
                                                            .toLowerCase();

              return repo;
            });
            const repoDataset: IRepositoriesAttr[] = repos;
            const handleMtUpdateRepoRes: ((mtResult: IUpdateRepoAttr) => void) = (mtResult: IUpdateRepoAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.updateResources.success) {
                  hidePreloader();
                  mixpanel.track(
                    "RemoveProjectRepo",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success_change"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtAddReposRes: ((mtResult: IAddReposAttr) => void) = (mtResult: IAddReposAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.addResources.success) {
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
            let auxRepo: {[value: string]: string | null} | undefined;

            return (
              <React.Fragment>
              <Mutation mutation={UPDATE_RESOURCE_MUTATION} onCompleted={handleMtUpdateRepoRes}>
                  { (updateRepositories: MutationFn<IUpdateRepoAttr,
                    {projectName: string; resData: string; resType: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }
                      if (!_.isUndefined(mutationRes.error)) {
                        hidePreloader();
                        handleGraphQLErrors("An error occurred removing repositories", mutationRes.error);

                        return <React.Fragment/>;
                      }

                      const changeSwitchButtonStatus: (() => void) = (): void => {
                        if (auxRepo !== undefined && auxRepo.urlRepo !== null) {
                          const button: Element | undefined = findSwitchButton(auxRepo.urlRepo, "repository");
                          if (button !== undefined &&
                            ((auxRepo.state === "INACTIVE" && button.classList.contains("on")) ||
                             (auxRepo.state === "ACTIVE" && button.classList.contains("off")))) {
                            changeSwitchButtonState(button);
                          }
                        }
                      };

                      const handleUpdateRepoStateClick: (() => void) = (): void => {
                        updateRepositories({ variables: {
                          projectName,
                          resData: JSON.stringify(auxRepo),
                          resType: "repository"}},
                        )
                          .catch();
                        if (auxRepo !== undefined) {
                          auxRepo.state = auxRepo.state === "INACTIVE" ? "ACTIVE" : "INACTIVE";
                        }
                        changeSwitchButtonStatus();
                      };

                      const handleUpdateRepoStateClickRevert: (() => void) = (): void => {
                        changeSwitchButtonStatus();
                      };

                      const handleUpdateRepo: ((repoInfo: { [key: string]: string } | undefined) => void) =
                      (repoInfo: { [key: string]: string } | undefined): void => {
                        if (repoInfo !== undefined) {
                          let repoLastState: string = repoInfo.state;
                          const button: Element | undefined = findSwitchButton(repoInfo.urlRepo, "repository");
                          if (button !== undefined) {
                            repoLastState = getSwitchButtonState(button) ? "ACTIVE" : "INACTIVE";
                          }
                          const repoUpdated: {[value: string]: string | null} = {
                            branch: repoInfo.branch,
                            protocol: repoInfo.protocol,
                            state: repoLastState,
                            urlRepo: repoInfo.urlRepo,
                          };
                          auxRepo = repoUpdated;
                          props.onOpenChangeRepoStateModal();
                        }
                      };

                      return(
                        <React.Fragment>
                        <Row>
                          <Col md={12} sm={12}>
                            <DataTable
                              dataset={repoDataset}
                              selectionMode="radio"
                              enableRowSelection={false}
                              exportCsv={true}
                              search={true}
                              headers={[
                                {
                                  dataField: "protocol",
                                  header: translate.t("search_findings.repositories_table.protocol"),
                                  isDate: false,
                                  isStatus: false,
                                  width: "14%",
                                  wrapped: true,
                                },
                                {
                                  dataField: "urlRepo",
                                  header: translate.t("search_findings.repositories_table.repository"),
                                  isDate: false,
                                  isStatus: false,
                                  width: "56%",
                                  wrapped: true,
                                },
                                {
                                  dataField: "branch",
                                  header: translate.t("search_findings.repositories_table.branch"),
                                  isDate: false,
                                  isStatus: false,
                                  width: "18%",
                                  wrapped: true,
                                },
                                {
                                  align: "center",
                                  changeFunction: currUserRole === "customer" ? handleUpdateRepo : undefined,
                                  dataField: "state",
                                  header: translate.t("search_findings.repositories_table.state"),
                                  isDate: false,
                                  isStatus: currUserRole === "customer" ? false : true,
                                  width: "12%",
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
                              {currUserRole === "customer" ?
                              <Button
                                id="addRepository"
                                block={true}
                                bsStyle="primary"
                                onClick={handleAddRepoClick}
                              >
                                <Glyphicon glyph="plus"/>&nbsp;
                                {translate.t("search_findings.tab_resources.add_repository")}
                              </Button> : undefined}
                              </Col>
                          </Col>
                          <Col md={12}>
                            <br />
                            <label style={{fontSize: "15px"}}>
                              <b>{translate.t("search_findings.tab_resources.total_repos")}</b>
                              {repoDataset.length}
                            </label>
                          </Col>
                        </Row>

                        <ConfirmDialog
                          name="openChangeRepoStateModal"
                          onProceed={handleUpdateRepoStateClick}
                          onNotProceed={handleUpdateRepoStateClickRevert}
                          title="Repository change state"
                          closeOnProceed={true}
                        />
                      </React.Fragment>);
                    }}
                </Mutation>
                <Mutation mutation={ADD_RESOURCE_MUTATION} onCompleted={handleMtAddReposRes}>
                { (addRepositories: MutationFn<IAddReposAttr, {projectName: string; resData: string; resType: string}>,
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
                          addRepositories({variables: {
                            projectName,
                            resData: JSON.stringify(values.resources),
                            resType: "repository"}},
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
              </React.Fragment>);
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
            let envs: IEnvironmentsAttr[] = JSON.parse(data.resources.environments);
            envs = envs.map((env: IEnvironmentsAttr) => {
              env.state = "ACTIVE";
              if ("historic_state" in env) {
                env.state = env.historic_state[env.historic_state.length - 1].state;
              }
              env.state = env.state.charAt(0) + env.state.slice(1)
                                                         .toLowerCase();

              return env;
            });
            const envDataset: IEnvironmentsAttr[] = envs;

            const handleMtUpdateEnvRes: ((mtResult: IUpdateEnvAttr) => void) = (mtResult: IUpdateEnvAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.updateResources.success) {
                  hidePreloader();
                  mixpanel.track(
                    "RemoveProjectEnv",
                    {
                      Organization: (window as Window & { userOrganization: string }).userOrganization,
                      User: (window as Window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success_change"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };

            const handleMtAddEnvsRes: ((mtResult: IAddEnvAttr) => void) = (mtResult: IAddEnvAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.addResources.success) {
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
            let auxEnv: {[value: string]: string | null} | undefined;

            return (
              <React.Fragment>
                <Mutation mutation={UPDATE_RESOURCE_MUTATION} onCompleted={handleMtUpdateEnvRes}>
                  { (updateResources: MutationFn<IUpdateEnvAttr,
                    {projectName: string; resData: string; resType: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }
                      if (!_.isUndefined(mutationRes.error)) {
                        hidePreloader();
                        handleGraphQLErrors("An error occurred removing environments", mutationRes.error);

                        return <React.Fragment/>;
                      }

                      const changeSwitchButtonStatus: (() => void) = (): void => {
                        if (auxEnv !== undefined && auxEnv.urlEnv !== null) {
                          const button: Element | undefined = findSwitchButton(auxEnv.urlEnv, "environment");
                          if (button !== undefined &&
                            ((auxEnv.state === "INACTIVE" && button.classList.contains("on")) ||
                              (auxEnv.state === "ACTIVE" && button.classList.contains("off")))) {
                            changeSwitchButtonState(button);
                          }
                        }
                      };

                      const handleUpdateEnvStateClick: (() => void) = (): void => {
                        updateResources({ variables: { projectName,
                                                       resData: JSON.stringify(auxEnv),
                                                       resType: "environment"} })
                          .catch();
                        if (auxEnv !== undefined) {
                          auxEnv.state = auxEnv.state === "INACTIVE" ? "ACTIVE" : "INACTIVE";
                        }
                        changeSwitchButtonStatus();
                      };

                      const handleUpdateEnvStateClickRevert: (() => void) = (): void => {
                        changeSwitchButtonStatus();
                      };

                      const handleUpdateEnv: ((envInfo: { [key: string]: string } | undefined) => void) =
                      (envInfo: { [key: string]: string } | undefined): void => {
                        if (envInfo !== undefined) {
                          let envLastState: string = envInfo.state;
                          const button: Element | undefined = findSwitchButton(envInfo.urlEnv, "environment");
                          if (button !== undefined) {
                            envLastState = getSwitchButtonState(button) ? "ACTIVE" : "INACTIVE";
                          }
                          const envUpdated: {[value: string]: string | null} = {
                            state: envLastState,
                            urlEnv: envInfo.urlEnv,
                          };
                          auxEnv = envUpdated;
                          props.onOpenChangeEnvStateModal();
                        }
                      };

                      return (
                        <React.Fragment>
                        <Row>
                          <Col md={12} sm={12}>
                            <DataTable
                              dataset={envDataset}
                              selectionMode="radio"
                              enableRowSelection={false}
                              exportCsv={true}
                              search={true}
                              headers={[
                                {
                                  dataField: "urlEnv",
                                  header: translate.t("search_findings.environment_table.environment"),
                                  isDate: false,
                                  isStatus: false,
                                  wrapped: true,
                                },
                                {
                                  align: "center",
                                  changeFunction: currUserRole === "customer" ? handleUpdateEnv : undefined,
                                  dataField: "state",
                                  header: translate.t("search_findings.repositories_table.state"),
                                  isDate: false,
                                  isStatus: currUserRole === "customer" ? false : true,
                                  width: "12%",
                                  wrapped: true,
                                },
                              ]}
                              id="tblRepositories"
                              pageSize={15}
                              title={translate.t("search_findings.tab_resources.environments_title")}
                            />
                          </Col>
                          <Col md={12}>
                          <br />
                          <Col mdOffset={4} md={2} sm={6}>
                            {currUserRole === "customer" ?
                            <Button
                              id="addEnvironment"
                              block={true}
                              bsStyle="primary"
                              onClick={handleAddEnvClick}
                            >
                              <Glyphicon glyph="plus"/>&nbsp;
                              {translate.t("search_findings.tab_resources.add_repository")}
                            </Button> : undefined}
                          </Col>
                          </Col>
                          <Col md={12}>
                            <br />
                            <label style={{fontSize: "15px"}}>
                              <b>{translate.t("search_findings.tab_resources.total_envs")}</b>
                              {envDataset.length}
                            </label>
                          </Col>
                        </Row>
                        <ConfirmDialog
                          name="openChangeEnvStateModal"
                          onProceed={handleUpdateEnvStateClick}
                          onNotProceed={handleUpdateEnvStateClickRevert}
                          title="Environment change state"
                          closeOnProceed={true}
                        />
                        </React.Fragment>
                      );
                    }}
                </Mutation>
                <Mutation mutation={ADD_RESOURCE_MUTATION} onCompleted={handleMtAddEnvsRes}>
                  { (addResources: MutationFn<IAddEnvAttr, {projectName: string; resData: string; resType: string}>,
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
                            addResources({
                              variables: { projectName,
                                           resData: JSON.stringify(values.resources),
                                           resType: "environment"},
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
              {currUserRole === "customer" ?
              <Button
                id="addFile"
                block={true}
                bsStyle="primary"
                onClick={handleAddFileClick}
              >
                <Glyphicon glyph="plus"/>&nbsp;
                {translate.t("search_findings.tab_resources.add_repository")}
              </Button> : undefined}
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
          canRemove={currUserRole === "customer" ? true : false}
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
      {renderRepositories(props)}
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
      onOpenChangeEnvStateModal: (): void => { dispatch(openConfirmDialog("openChangeEnvStateModal")); },
      onOpenChangeRepoStateModal: (): void => { dispatch(openConfirmDialog("openChangeRepoStateModal")); },
      onOpenEnvsModal: (): void => { dispatch(actions.openAddEnvModal()); },
      onOpenFilesModal: (): void => { dispatch(actions.openAddFilesModal()); },
      onOpenOptionsModal: (row: string): void => { dispatch(actions.openOptionsModal(row)); },
      onOpenReposModal: (): void => { dispatch(actions.openAddRepoModal()); },
      onOpenTagsModal: (): void => { dispatch(actions.openTagsModal()); },
      onSaveFiles: (files: IResourcesViewProps["files"]): void => { dispatch(actions.saveFiles(projectName, files)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectResourcesView));
