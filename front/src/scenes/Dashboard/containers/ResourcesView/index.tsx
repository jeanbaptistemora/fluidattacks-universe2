/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { Button } from "../../../../components/Button/index";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidFileName } from "../../../../utils/validations";
import { addResourcesModal as AddResourcesModal } from "../../components/AddResourcesModal/index";
import { fileOptionsModal as FileOptionsModal } from "../../components/FileOptionsModal/index";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";

type IResourcesViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

interface IResourcesViewStateProps {
  addModal: {
    open: boolean;
    type: "repository" | "environment" | "file";
  };
  environments: Array<{ urlEnv: string }>;
  files: Array<{ description: string; fileName: string }>;
  optionsModal: {
    open: boolean;
    rowInfo: { fileName: string };
  };
  repositories: Array<{ branch: string; urlRepo: string }>;
}

type IResourcesViewProps = IResourcesViewBaseProps & (IResourcesViewStateProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IResourcesViewProps, {}>({
  componentDidMount(): void {
    const { projectName } = this.props.match.params;
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadResources(projectName));
  },
});

const removeRepo: ((arg1: string) => void) = (projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblRepositories tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const repository: string | null = selectedRow.children[1].textContent;
      const branch: string | null = selectedRow.children[2].textContent;

      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.removeRepo(projectName, repository, branch));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing repositories");
    }
  } else {
    msgError(translate.t("search_findings.tab_resources.no_selection"));
  }
};

const saveRepos: (
  (resources: IResourcesViewProps["repositories"], projectName: string,
   currentRepos: IResourcesViewProps["repositories"],
  ) => void) =
  (resources: IResourcesViewProps["repositories"], projectName: string,
   currentRepos: IResourcesViewProps["repositories"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = resources.filter(
      (newItem: IResourcesViewProps["repositories"][0]) => _.findIndex(
        currentRepos,
        (currentItem: IResourcesViewProps["repositories"][0]) =>
          currentItem.urlRepo === newItem.urlRepo && currentItem.branch === newItem.branch,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.saveRepos(projectName, resources));
    }
  };

const removeEnv: ((arg1: string) => void) = (projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblEnvironments tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const env: string | null = selectedRow.children[1].textContent;
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.removeEnv(projectName, env));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing environments");
    }
  } else {
    msgError(translate.t("search_findings.tab_resources.no_selection"));
  }
};

const saveEnvs: (
  (resources: IResourcesViewProps["environments"], projectName: string,
   currentEnvs: IResourcesViewProps["environments"],
  ) => void) =
  (resources: IResourcesViewProps["environments"], projectName: string,
   currentEnvs: IResourcesViewProps["environments"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = resources.filter(
      (newItem: IResourcesViewProps["environments"][0]) => _.findIndex(
        currentEnvs,
        (currentItem: IResourcesViewProps["environments"][0]) =>
          currentItem.urlEnv === newItem.urlEnv,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.saveEnvs(projectName, resources));
    }
  };

const removeFiles: ((arg1: string, arg2: { fileName: string | null}) => void) =
  (projectName: string, rowInfo: { fileName: string | null}): void => {
    if (rowInfo.fileName !== null) {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.deleteFile(projectName, rowInfo.fileName));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing files");
    }
  };

const saveFiles: ((files: IResourcesViewProps["files"], projectName: string, currentFiles: IResourcesViewProps["files"])
  => void) =
  (files: IResourcesViewProps["files"], projectName: string, currentFiles: IResourcesViewProps["files"]): void => {
    const selected: FileList | null = (document.querySelector("#file") as HTMLInputElement).files;
    if (_.isNil(selected) || selected.length === 0) {
      msgError(translate.t("proj_alerts.no_file_selected"));
      throw new Error();
    } else {
      files[0].fileName = selected[0].name;
    }
    if (isValidFileName(files[0].fileName)) {
      let containsRepeated: boolean;
      containsRepeated = files.filter(
        (newItem: IResourcesViewProps["files"][0]) => _.findIndex(
          currentFiles,
          (currentItem: IResourcesViewProps["files"][0]) =>
            currentItem.fileName === newItem.fileName,
        ) > -1).length > 0;
      if (containsRepeated) {
        msgError(translate.t("search_findings.tab_resources.repeated_item"));
      } else {
        const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
          store.dispatch as ThunkDispatch<{}, {}, AnyAction>
        );
        thunkDispatch(actions.saveFiles(projectName, files));
      }
    } else {
      msgError(translate.t("search_findings.tab_resources.invalid_chars"));
    }
  };

const downloadFile: ((arg1: string, arg2: { fileName: string | null}) => void) =
  (projectName: string, rowInfo: { fileName: string | null}): void => {
    if (rowInfo.fileName !== null) {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.downloadFile(projectName, rowInfo.fileName));
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred downloading file");
    }
  };

const projectResourcesView: React.StatelessComponent<IResourcesViewProps> =
  (props: IResourcesViewProps): JSX.Element => {
    const { projectName } = props.match.params;

    let onSubmitFunction: (((values: { resources: IResourcesViewProps["environments"] }) => void)
      | ((values: { resources: IResourcesViewProps["repositories"] }) => void)
      | ((values: { resources: IResourcesViewProps["files"] }) => void));
    if (props.addModal.type === "environment") {
      onSubmitFunction = (values: { resources: IResourcesViewProps["environments"] }): void => {
        saveEnvs(values.resources, projectName, props.environments);
      };
    } else if (props.addModal.type === "repository") {
      onSubmitFunction = (values: { resources: IResourcesViewProps["repositories"] }): void => {
        saveRepos(values.resources, projectName, props.repositories);
      };
    } else {
      onSubmitFunction = (values: { resources: IResourcesViewProps["files"] }): void => {
        saveFiles(values.resources, projectName, props.files);
      };
    }

    return (
  <React.StrictMode>
    <div id="resources" className="tab-pane cont active">
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12}>
                  <Col mdOffset={4} md={2} sm={6}>
                    <Button
                      id="addRepository"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { store.dispatch(actions.openAddModal("repository")); }}
                    >
                      <Glyphicon glyph="plus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.add_repository")}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button
                      id="removeRepository"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeRepo(projectName); }}
                    >
                      <Glyphicon glyph="minus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.remove_repository")}
                    </Button>
                  </Col>
                </Col>
              </Row>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={props.repositories}
                    onClickRow={(): void => {}}
                    enableRowSelection={true}
                    exportCsv={true}
                    search={true}
                    headers={[
                      {
                        dataField: "urlRepo",
                        header: translate.t("search_findings.repositories_table.repository"),
                        isDate: false,
                        isStatus: false,
                        width: "70%",
                        wrapped: true,
                      },
                      {
                        dataField: "branch",
                        header: translate.t("search_findings.repositories_table.branch"),
                        isDate: false,
                        isStatus: false,
                        width: "30%",
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
                  <label style={{fontSize: "15px"}}>
                    <b>{translate.t("search_findings.tab_resources.total_repos")}</b>
                    {props.repositories.length}
                  </label>
                </Col>
              </Row>
            </Col>
          </Row>
        </Col>
      </Row>
      <hr/>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Row>
            <Col md={12} sm={12} xs={12}>
              <Row>
                <Col md={12}>
                  <Col mdOffset={4} md={2} sm={6}>
                    <Button
                      id="addEnvironment"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { store.dispatch(actions.openAddModal("environment")); }}
                    >
                      <Glyphicon glyph="plus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.add_repository")}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button
                      id="removeEnvironment"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeEnv(projectName); }}
                    >
                      <Glyphicon glyph="minus"/>&nbsp;
                      {translate.t("search_findings.tab_resources.remove_repository")}
                    </Button>
                  </Col>
                </Col>
              </Row>
              <Row>
                <Col md={12} sm={12}>
                  <DataTable
                    dataset={props.environments}
                    onClickRow={(): void => {}}
                    enableRowSelection={true}
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
                    ]}
                    id="tblEnvironments"
                    pageSize={15}
                    title={translate.t("search_findings.tab_resources.environments_title")}
                  />
                </Col>
                <Col md={12}>
                  <br />
                  <label style={{fontSize: "15px"}}>
                    <b>{translate.t("search_findings.tab_resources.total_envs")}</b>
                    {props.environments.length}
                  </label>
                </Col>
              </Row>
            </Col>
          </Row>
        </Col>
      </Row>
      <hr/>
        <Row>
          <Col md={12} sm={12} xs={12}>
            <Row>
              <Col md={12} sm={12} xs={12}>
                <Row>
                  <Col md={12}>
                    <Col mdOffset={4} md={2} sm={6}>
                      <Button
                        id="addFile"
                        block={true}
                        bsStyle="primary"
                        onClick={(): void => { store.dispatch(actions.openAddModal("file")); }}
                      >
                        <Glyphicon glyph="plus"/>&nbsp;
                        {translate.t("search_findings.tab_resources.add_repository")}
                      </Button>
                    </Col>
                  </Col>
                </Row>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTable
                      dataset={props.files}
                      onClickRow={(row: string | undefined): void => {store.dispatch(actions.openOptionsModal(row)); }}
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
                    <label style={{fontSize: "15px"}}>
                      <b>{translate.t("search_findings.tab_resources.total_files")}</b>
                      {props.files.length}
                    </label>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
      <AddResourcesModal
        isOpen={props.addModal.open}
        type={props.addModal.type}
        onClose={(): void => { store.dispatch(actions.closeAddModal()); }}
        onSubmit={onSubmitFunction}
      />
      <FileOptionsModal
        fileName={props.optionsModal.rowInfo.fileName}
        isOpen={props.optionsModal.open}
        onClose={(): void => { store.dispatch(actions.closeOptionsModal()); }}
        onSubmit={onSubmitFunction}
        onDelete={(): void => {removeFiles(projectName, props.optionsModal.rowInfo); }}
        onDownload={(): void => {downloadFile(projectName, props.optionsModal.rowInfo); }}
      />
    </div>
  </React.StrictMode>
); };

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IResourcesViewStateProps, IResourcesViewBaseProps, IState> =
  (state: IState): IResourcesViewStateProps => ({
    addModal: state.dashboard.resources.addModal,
    environments: state.dashboard.resources.environments,
    files: state.dashboard.resources.files,
    optionsModal: state.dashboard.resources.optionsModal,
    repositories: state.dashboard.resources.repositories,
  });

const mapDispatchToProps: undefined = undefined;

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectResourcesView));
