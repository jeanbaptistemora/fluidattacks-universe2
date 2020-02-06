/* tslint:disable:jsx-no-multiline-js max-file-line-count
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 * MAX-FILE-LINE-COUNT: this file exceeds by 22 the maximum of 1000 lines
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { Trans } from "react-i18next";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { ConfirmDialog, ConfirmFn } from "../../../../components/ConfirmDialog/index";
import { DataTableNext } from "../../../../components/DataTableNext";
import { changeFormatter, statusFormatter } from "../../../../components/DataTableNext/formatters";
import { default as globalStyle } from "../../../../styles/global.css";
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
import { RemoveProjectModal } from "../../components/RemoveProjectModal";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import {
  ADD_RESOURCE_MUTATION, ADD_TAGS_MUTATION, GET_ENVIRONMENTS, GET_PROJECT_DATA, GET_REPOSITORIES, GET_TAGS,
  REMOVE_TAG_MUTATION, UPDATE_RESOURCE_MUTATION,
} from "./queries";
import {
  IAddEnvAttr, IAddReposAttr, IAddTagsAttr, IEnvironmentsAttr, IGetProjectData, IProjectTagsAttr, IRemoveTagsAttr,
  IRepositoriesAttr, IResourcesAttr, IResourcesViewBaseProps, IResourcesViewDispatchProps, IResourcesViewProps,
  IResourcesViewStateProps, IUpdateEnvAttr, IUpdateRepoAttr,
} from "./types";

const enhance: InferableComponentEnhancer<{}> = lifecycle<IResourcesViewProps, {}>({
  componentDidMount(): void {
    mixpanel.track(
      "ProjectResources",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
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
            Organization: (window as typeof window & { userOrganization: string }).userOrganization,
            User: (window as typeof window & { userName: string }).userName,
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

const selectOptions: optionSelectFilterProps[] = [
  {value: "Active", label: "Active"},
  {value: "Inactive", label: "Inactive"},
];
const clearSelection: string = "_CLEAR_";

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

let currUserRole: string = "customer";
const allowedRoles: string[] = ["customer"];

const renderTagsView: ((props: IResourcesViewProps) => JSX.Element) = (props: IResourcesViewProps): JSX.Element => {
  const [sortValueTags, setSortValueTags] = React.useState(props.defaultSort.tags);
  const handleOpenTagsModal: (() => void) = (): void => { props.onOpenTagsModal(); };
  const handleCloseTagsModal: (() => void) = (): void => { props.onCloseTagsModal(); };
  const projectName: string = props.match.params.projectName;

  const handleQryResult: ((qrResult: IProjectTagsAttr) => void) = (qrResult: IProjectTagsAttr): void => {
    mixpanel.track(
      "ProjectTags",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
  };

  return (
    <Query
      query={GET_TAGS}
      variables={{ projectName }}
      onCompleted={handleQryResult}
    >
      {
        ({ error, data, refetch }: QueryResult<IProjectTagsAttr>): React.ReactNode => {
          if (_.isUndefined(data) || _.isEmpty(data)
          || (!_.isUndefined(data) && !_.isEmpty(data.project.deletionDate))) {

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting tags", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data) && !_.isEmpty(data.project.subscription) && _.isEmpty(data.project.deletionDate)) {
            const tagsDataset: Array<{ tagName: string }> = data.project.tags.map(
              (tagName: string) => ({ tagName }));

            const handleMtRemoveTagRes: ((mtResult: IRemoveTagsAttr) => void) = (mtResult: IRemoveTagsAttr): void => {
              if (!_.isUndefined(mtResult)) {
                if (mtResult.removeTag.success) {
                  refetch()
                      .catch();
                  mixpanel.track(
                    "RemoveProjectTags",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
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
                  mixpanel.track(
                    "AddProjectTags",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
                    });
                  msgSuccess(
                    translate.t("search_findings.tab_resources.success"),
                    translate.t("search_findings.tab_users.title_success"),
                  );
                }
              }
            };
            const onSortStateTags: ((dataField: string, order: SortOrder) => void) =
            (dataField: string, order: SortOrder): void => {
              const newSorted: Sorted = {dataField,  order};
              setSortValueTags(newSorted);
              const newValues: {} = {...props.defaultSort, tags: newSorted};
              props.onSort(newValues);
            };

            return (
              <React.Fragment>
                <hr/>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTableNext
                      bordered={true}
                      dataset={tagsDataset}
                      defaultSorted={sortValueTags}
                      exportCsv={false}
                      search={false}
                      headers={[
                        {
                          dataField: "tagName",
                          header: translate.t("search_findings.tab_resources.tags_title"),
                          onSort: onSortStateTags,
                        },
                      ]}
                      id="tblTags"
                      pageSize={15}
                      remote={false}
                      striped={true}
                      selectionMode={{
                        clickToSelect: allowedRoles.includes(currUserRole),
                        hideSelectColumn: !allowedRoles.includes(currUserRole),
                        mode: "radio",
                      }}
                      title={translate.t("search_findings.tab_resources.tags_title")}
                    />
                  </Col>
                  <Col md={12}>
                    <br />
                    <Col mdOffset={4} md={2} sm={6}>
                      {allowedRoles.includes(currUserRole) ?
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
                          if (!_.isUndefined(mutationRes.error)) {
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
                              {allowedRoles.includes(currUserRole) ?
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
                      if (!_.isUndefined(mutationRes.error)) {
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
    const [filterValueRepositories, setFilterValueRepositories] = React.useState(props.filters.stateRepositories);
    const [sortValueRepositories, setSortValueRepositories] = React.useState(props.defaultSort.repositories);
    const handleAddRepoClick: (() => void) = (): void => { props.onOpenReposModal(); };
    const handleCloseReposModalClick: (() => void) = (): void => { props.onCloseReposModal(); };
    const projectName: string = props.match.params.projectName;

    return (
      <Query query={GET_REPOSITORIES} variables={{ projectName }}>
      {
        ({ error, data, refetch }: QueryResult<IResourcesAttr>): React.ReactNode => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting repositories", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
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
                  refetch()
                    .catch();
                  mixpanel.track(
                    "RemoveProjectRepo",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
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
                  mixpanel.track(
                    "AddProjectRepo",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
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
                <ConfirmDialog title="Repository change state">
                  {(confirmStateChange: ConfirmFn): React.ReactNode => (
              <Mutation mutation={UPDATE_RESOURCE_MUTATION} onCompleted={handleMtUpdateRepoRes}>
                  { (updateRepositories: MutationFn<IUpdateRepoAttr,
                    {projectName: string; resData: string; resType: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (!_.isUndefined(mutationRes.error)) {
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

                      const handleUpdateRepo: ((repoInfo: { [key: string]: string } | undefined) => void) =
                      (repoInfo: { [key: string]: string } | undefined): void => {
                        if (repoInfo !== undefined) {
                          let repoLastState: string = repoInfo.state;
                          const button: Element | undefined = findSwitchButton(repoInfo.urlRepo, "repository");
                          if (button !== undefined) {
                            repoLastState = getSwitchButtonState(button) ? "ACTIVE" : "INACTIVE";
                          }
                          const repoUpdated: {[value: string]: string | null} = {
                            ...repoInfo,
                            state: repoLastState,
                          };
                          auxRepo = repoUpdated;

                          confirmStateChange(
                            () => {
                              updateRepositories({
                                variables: { projectName, resData: JSON.stringify(auxRepo), resType: "repository" },
                              })
                              .catch();
                            },
                            changeSwitchButtonStatus,
                          );
                        }
                      };

                      const onSortStateRepositories: ((dataField: string, order: SortOrder) => void) =
                      (dataField: string, order: SortOrder): void => {
                        const newSorted: Sorted = {dataField,  order};
                        setSortValueRepositories(newSorted);
                        const newValues: {} = {...props.defaultSort, repositories: newSorted};
                        props.onSort(newValues);
                      };

                      const onFilterInputs: ((filterVal: string) => void) = (filterVal: string): void => {
                        if (filterValueRepositories !== filterVal && clearSelection !== filterValueRepositories) {
                          setFilterValueRepositories(filterVal);
                          const newValues: {} = {...props.filters, stateRepositories: filterVal};
                          props.onFilter(newValues);
                        }
                      };

                      const clearFilterInputs: ((eventInput: React.FormEvent<HTMLInputElement>) => void) =
                      (eventInput: React.FormEvent<HTMLInputElement>): void => {
                        const inputValue: string = eventInput.currentTarget.value;
                        if (inputValue.length === 0) {
                          if (filterValueRepositories !== "") {
                            setFilterValueRepositories(clearSelection);
                            const newValues: {} = {...props.filters, stateRepositories: ""};
                            props.onFilter(newValues);
                          }
                        }
                      };

                      return(
                        <React.Fragment>
                        <Row>
                          <Col md={12} sm={12}>
                            <DataTableNext
                              bordered={true}
                              dataset={repoDataset}
                              defaultSorted={sortValueRepositories}
                              exportCsv={true}
                              search={true}
                              headers={[
                                {
                                  dataField: "protocol",
                                  header: translate.t("search_findings.repositories_table.protocol"),
                                  onSort: onSortStateRepositories,
                                  width: "14%",
                                  wrapped: true,
                                },
                                {
                                  dataField: "urlRepo",
                                  header: translate.t("search_findings.repositories_table.repository"),
                                  onSort: onSortStateRepositories,
                                  width: "56%",
                                  wrapped: true,
                                },
                                {
                                  dataField: "branch",
                                  header: translate.t("search_findings.repositories_table.branch"),
                                  onSort: onSortStateRepositories,
                                  width: "18%",
                                  wrapped: true,
                                },
                                {
                                  align: "center",
                                  changeFunction: allowedRoles.includes(currUserRole) ? handleUpdateRepo : undefined,
                                  dataField: "state",
                                  filter: selectFilter({
                                    defaultValue: filterValueRepositories,
                                    onFilter: onFilterInputs,
                                    onInput: clearFilterInputs,
                                    options: selectOptions,
                                  }),
                                  formatter: allowedRoles.includes(currUserRole) ? changeFormatter : statusFormatter,
                                  header: translate.t("search_findings.repositories_table.state"),
                                  onSort: onSortStateRepositories,
                                  width: "12%",
                                  wrapped: true,
                                },
                              ]}
                              id="tblRepositories"
                              pageSize={15}
                              remote={false}
                              striped={true}
                              title={translate.t("search_findings.tab_resources.repositories_title")}
                            />
                          </Col>
                          <Col md={12}>
                            <br />
                            <Col mdOffset={4} md={2} sm={6}>
                              {allowedRoles.includes(currUserRole) ?
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
                      </React.Fragment>);
                    }}
                </Mutation>
                )}
                </ConfirmDialog>
                <Mutation mutation={ADD_RESOURCE_MUTATION} onCompleted={handleMtAddReposRes}>
                { (addRepositories: MutationFn<IAddReposAttr, {projectName: string; resData: string; resType: string}>,
                   mutationRes: MutationResult): React.ReactNode => {
                    if (!_.isUndefined(mutationRes.error)) {
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
    const [filterValueEnvironments, setFilterValueEnvironments] = React.useState(props.filters.stateEnvironments);
    const [sortValueEnvironments, setSortValueEnvironments] = React.useState(props.defaultSort.environments);
    const handleAddEnvClick: (() => void) = (): void => { props.onOpenEnvsModal(); };
    const handleCloseEnvModalClick: (() => void) = (): void => { props.onCloseEnvsModal(); };
    const projectName: string = props.match.params.projectName;

    return (
      <Query query={GET_ENVIRONMENTS} variables={{ projectName }}>
      {
        ({ error, data, refetch }: QueryResult<IResourcesAttr>): React.ReactNode => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting environments", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
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
                  refetch()
                    .catch();
                  mixpanel.track(
                    "RemoveProjectEnv",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
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
                  mixpanel.track(
                    "AddProjectEnv",
                    {
                      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
                      User: (window as typeof window & { userName: string }).userName,
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
                <ConfirmDialog title="Environment change state">
                  {(confirmStateChange: ConfirmFn): React.ReactNode => (
                <Mutation mutation={UPDATE_RESOURCE_MUTATION} onCompleted={handleMtUpdateEnvRes}>
                  { (updateResources: MutationFn<IUpdateEnvAttr,
                    {projectName: string; resData: string; resType: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (!_.isUndefined(mutationRes.error)) {
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

                      const handleUpdateEnv: ((envInfo: { [key: string]: string } | undefined) => void) =
                      (envInfo: { [key: string]: string } | undefined): void => {
                        if (envInfo !== undefined) {
                          let envLastState: string = envInfo.state;
                          const button: Element | undefined = findSwitchButton(envInfo.urlEnv, "environment");
                          if (button !== undefined) {
                            envLastState = getSwitchButtonState(button) ? "ACTIVE" : "INACTIVE";
                          }
                          const envUpdated: {[value: string]: string | null} = {
                            ...envInfo,
                            state: envLastState,
                          };
                          auxEnv = envUpdated;

                          confirmStateChange(
                            () => {
                              updateResources({
                                variables: {
                                  projectName,
                                  resData: JSON.stringify(auxEnv),
                                  resType: "environment",
                                },
                              })
                                .catch();
                            },
                            changeSwitchButtonStatus,
                          );
                        }
                      };
                      const onSortStateEnviroments: ((dataField: string, order: SortOrder) => void) =
                      (dataField: string, order: SortOrder): void => {
                        const newSorted: Sorted = {dataField,  order};
                        setSortValueEnvironments(newSorted);
                        const newValues: {} = {...props.defaultSort, environments: newSorted};
                        props.onSort(newValues);
                      };
                      const onFilterInputs: ((filterVal: string) => void) = (filterVal: string): void => {
                        if (filterValueEnvironments !== filterVal && clearSelection !== filterValueEnvironments) {
                          setFilterValueEnvironments(filterVal);
                          const newValues: {} = {...props.filters, stateEnvironments: filterVal};
                          props.onFilter(newValues);
                        }
                      };

                      const clearFilterInputs: ((eventInput: React.FormEvent<HTMLInputElement>) => void) =
                      (eventInput: React.FormEvent<HTMLInputElement>): void => {
                        const inputValue: string = eventInput.currentTarget.value;
                        if (inputValue.length === 0) {
                          if (filterValueEnvironments !== "") {
                            setFilterValueEnvironments(clearSelection);
                            const newValues: {} = {...props.filters, stateEnvironments: ""};
                            props.onFilter(newValues);
                          }
                        }
                      };

                      return (
                        <React.Fragment>
                        <Row>
                          <Col md={12} sm={12}>
                            <DataTableNext
                              bordered={true}
                              dataset={envDataset}
                              defaultSorted={sortValueEnvironments}
                              exportCsv={true}
                              search={true}
                              headers={[
                                {
                                  dataField: "urlEnv",
                                  header: translate.t("search_findings.environment_table.environment"),
                                  onSort: onSortStateEnviroments,
                                  wrapped: true,
                                },
                                {
                                  align: "center",
                                  changeFunction: allowedRoles.includes(currUserRole) ? handleUpdateEnv : undefined,
                                  dataField: "state",
                                  filter: selectFilter({
                                    defaultValue: filterValueEnvironments,
                                    onFilter: onFilterInputs,
                                    onInput: clearFilterInputs,
                                    options: selectOptions,
                                  }),
                                  formatter: allowedRoles.includes(currUserRole) ? changeFormatter : statusFormatter,
                                  header: translate.t("search_findings.repositories_table.state"),
                                  onSort: onSortStateEnviroments,
                                  width: "12%",
                                  wrapped: true,
                                },
                              ]}
                              id="tblRepositories"
                              pageSize={15}
                              remote={false}
                              striped={true}
                              title={translate.t("search_findings.tab_resources.environments_title")}
                            />
                          </Col>
                          <Col md={12}>
                          <br />
                          <Col mdOffset={4} md={2} sm={6}>
                            {allowedRoles.includes(currUserRole) ?
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
                        </React.Fragment>
                      );
                    }}
                </Mutation>
                )}
                </ConfirmDialog>
                <Mutation mutation={ADD_RESOURCE_MUTATION} onCompleted={handleMtAddEnvsRes}>
                  { (addResources: MutationFn<IAddEnvAttr, {projectName: string; resData: string; resType: string}>,
                     mutationRes: MutationResult): React.ReactNode => {
                      if (!_.isUndefined(mutationRes.error)) {
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
    const [sortValueFiles, setSortValueFiles] = React.useState(props.defaultSort.files);
    const handleAddFileClick: (() => void) = (): void => { props.onOpenFilesModal(); };
    const handleCloseFilesModalClick: (() => void) = (): void => { props.onCloseFilesModal(); };
    const handleCloseOptionsModalClick: (() => void) = (): void => { props.onCloseOptionsModal(); };
    const handleDeleteFileClick: (() => void) = (): void => {
      mixpanel.track(
        "RemoveProjectFiles",
        {
          Organization: (window as typeof window & { userOrganization: string }).userOrganization,
          User: (window as typeof window & { userName: string }).userName,
        });
      props.onDeleteFile(props.optionsModal.rowInfo.fileName);
    };
    const handleDownloadFileClick: (() => void) = (): void => {
      props.onDownloadFile(props.optionsModal.rowInfo.fileName);
    };
    const handleFileRowClick: ((event: React.FormEvent<HTMLButtonElement>, row: string) => void) =
    (event: React.FormEvent<HTMLButtonElement>, row: string): void => { props.onOpenOptionsModal(row); };

    const handleAddFile: ((values: IResourcesViewProps["files"][0]) => void) = (
      values: IResourcesViewProps["files"][0]): void => {
      handleSaveFiles([{ description: values.description, fileName: "", uploadDate: "" }], props);
    };
    const onSortStateFiles: ((dataField: string, order: SortOrder) => void) =
    (dataField: string, order: SortOrder): void => {
      const newSorted: Sorted = {dataField,  order};
      setSortValueFiles(newSorted);
      const newValues: {} = {...props.defaultSort, files: newSorted};
      props.onSort(newValues);
    };

    return (
      <React.Fragment>
        <hr/>
        <Row>
          <Col md={12} sm={12}>
            <DataTableNext
              bordered={true}
              dataset={props.files}
              defaultSorted={sortValueFiles}
              exportCsv={false}
              search={true}
              headers={[
                {
                  dataField: "fileName",
                  header: translate.t("search_findings.files_table.file"),
                  onSort: onSortStateFiles,
                  width: "25%",
                  wrapped: true,
                },
                {
                  dataField: "description",
                  header: translate.t("search_findings.files_table.description"),
                  onSort: onSortStateFiles,
                  width: "50%",
                  wrapped: true,
                },
                {
                  dataField: "uploadDate",
                  header: translate.t("search_findings.files_table.upload_date"),
                  onSort: onSortStateFiles,
                  width: "25%",
                  wrapped: true,
                },
              ]}
              id="tblFiles"
              pageSize={15}
              remote={false}
              rowEvents={{onClick: handleFileRowClick}}
              striped={true}
              title={translate.t("search_findings.tab_resources.files_title")}
            />
          </Col>
          <Col md={12}>
            <br />
            <Col mdOffset={5} md={2} sm={6}>
              {allowedRoles.includes(currUserRole) ?
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
          canRemove={allowedRoles.includes(currUserRole) ? true : false}
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
const renderDeleteBtn: ((props: IResourcesViewProps) => JSX.Element) = (props: IResourcesViewProps): JSX.Element => {
  const projectName: string = props.match.params.projectName;
  const [isProjectModalOpen, setProjectModalOpen] = React.useState(false);
  const openRemoveProjectModal: (() => void) = (): void => {
    setProjectModalOpen(true);
  };
  const closeRemoveProjectModal: (() => void) = (): void => {
    setProjectModalOpen(false);
  };

  return (
    <Query query={GET_PROJECT_DATA} variables={{ projectName }}>
    {
      ({ data }: QueryResult<IGetProjectData>): React.ReactNode => {
        if (_.isUndefined(data) || _.isEmpty(data)
        || (!_.isUndefined(data) && !_.isEmpty(data.project.deletionDate))) {
          return <React.Fragment />;
        }
        if (!_.isUndefined(data) && _.isEmpty(data.project.deletionDate)) {
          return (
            <React.Fragment>
              <hr/>
              <Row>
                <Col md={12}>
                  <h3 className={globalStyle.title}>{translate.t("search_findings.tab_resources.removeProject")}</h3>
                </Col>
                <Col md={12}>
                  <Trans>
                    {translate.t("search_findings.tab_resources.warningMessage")}
                  </Trans>
                </Col>
              </Row>
              <Row>
                <br />
                <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      <Button onClick={openRemoveProjectModal}>
                        <Glyphicon glyph="minus" />&nbsp;{translate.t("search_findings.tab_resources.removeProject")}
                      </Button>
                    </ButtonToolbar>
                    <RemoveProjectModal
                      isOpen={isProjectModalOpen}
                      onClose={closeRemoveProjectModal}
                      projectName={projectName.toLowerCase()}
                    />
                </Col>
              </Row>
            </React.Fragment>
          );
        }
      }}
    </Query>

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
      {_.includes(["admin"], (window as typeof window & { userRole: string }).userRole) ? renderDeleteBtn(props)
        : undefined}
    </div>
  </React.StrictMode>
  );

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IResourcesViewStateProps, IResourcesViewBaseProps, IState> =
  (state: IState): IResourcesViewStateProps => ({
    defaultSort: state.dashboard.resources.defaultSort,
    envModal: state.dashboard.resources.envModal,
    files: state.dashboard.resources.files,
    filesModal: state.dashboard.resources.filesModal,
    filters: state.dashboard.resources.filters,
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
      onFilter: (newValues: {}): void => {dispatch(actions.changeFilterValues(newValues)); },
      onLoad: (): void => {
        dispatch(actions.loadResources(projectName));
      },
      onOpenEnvsModal: (): void => { dispatch(actions.openAddEnvModal()); },
      onOpenFilesModal: (): void => { dispatch(actions.openAddFilesModal()); },
      onOpenOptionsModal: (row: string): void => { dispatch(actions.openOptionsModal(row)); },
      onOpenReposModal: (): void => { dispatch(actions.openAddRepoModal()); },
      onOpenTagsModal: (): void => { dispatch(actions.openTagsModal()); },
      onSaveFiles: (files: IResourcesViewProps["files"]): void => { dispatch(actions.saveFiles(projectName, files)); },
      onSort: (newValues: {}): void => {dispatch(actions.changeSortedValues(newValues)); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectResourcesView));
