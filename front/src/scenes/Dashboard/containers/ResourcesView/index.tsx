/* tslint:disable:jsx-no-lambda jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import _ from "lodash";
import React, { ComponentType } from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { addResourcesModal as AddResourcesModal } from "../../components/AddResourcesModal/index";
import * as actions from "./actions";

export interface IResourcesViewProps {
  addModal: {
    open: boolean;
    type: "repository" | "environment" | "file";
  };
  environmentsDataset: Array<{ urlEnv: string }>;
  filesDataset: Array<{ description: string; fileName: string }>;
  projectName: string;
  repositoriesDataset: Array<{ branch: string; urlRepo: string }>;
  showFiles: boolean;
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { projectName } = this.props as IResourcesViewProps;
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
  (resources: IResourcesViewProps["repositoriesDataset"],
   projectName: IResourcesViewProps["projectName"],
   currentRepos: IResourcesViewProps["repositoriesDataset"],
  ) => void) =
  (resources: IResourcesViewProps["repositoriesDataset"],
   projectName: IResourcesViewProps["projectName"],
   currentRepos: IResourcesViewProps["repositoriesDataset"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = resources.filter(
      (newItem: IResourcesViewProps["repositoriesDataset"][0]) => _.findIndex(
        currentRepos,
        (currentItem: IResourcesViewProps["repositoriesDataset"][0]) =>
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
  (resources: IResourcesViewProps["environmentsDataset"], projectName: IResourcesViewProps["projectName"],
   currentEnvs: IResourcesViewProps["environmentsDataset"],
  ) => void) =
  (resources: IResourcesViewProps["environmentsDataset"], projectName: IResourcesViewProps["projectName"],
   currentEnvs: IResourcesViewProps["environmentsDataset"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = resources.filter(
      (newItem: IResourcesViewProps["environmentsDataset"][0]) => _.findIndex(
        currentEnvs,
        (currentItem: IResourcesViewProps["environmentsDataset"][0]) =>
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

const saveFiles: (
  (files: IResourcesViewProps["filesDataset"],
   projectName: IResourcesViewProps["projectName"],
   currentFiles: IResourcesViewProps["filesDataset"],
  ) => void) =
  (files: IResourcesViewProps["filesDataset"],
   projectName: IResourcesViewProps["projectName"],
   currentFiles: IResourcesViewProps["filesDataset"],
  ): void => {
    const selected: FileList | null = (document.querySelector("#file") as HTMLInputElement).files;
    if (_.isNil(selected) || selected.length === 0) {
      msgError(translate.t("proj_alerts.no_file_selected"));
      throw new Error();
    } else {
      files[0].fileName = selected[0].name;
    }
    let containsRepeated: boolean;
    containsRepeated = files.filter(
      (newItem: IResourcesViewProps["filesDataset"][0]) => _.findIndex(
        currentFiles,
        (currentItem: IResourcesViewProps["filesDataset"][0]) =>
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
  };

const downloadFile: ((arg1: string) => void) = (projectName: string): void => {
    const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblFiles tr input:checked");
    if (selectedQry.length > 0) {
      if (selectedQry[0].closest("tr") !== null) {
        const selectedRow: Element = selectedQry[0].closest("tr") as Element;
        const file: string | null = selectedRow.children[1].textContent;
        const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
          store.dispatch as ThunkDispatch<{}, {}, AnyAction>
        );
        thunkDispatch(actions.downloadFile(projectName, file));
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error("An error occurred downloading file");
      }
    } else {
      msgError(translate.t("search_findings.tab_resources.no_selection"));
    }
  };

const mapStateToProps: ((arg1: StateType<Reducer>) => IResourcesViewProps) =
  (state: StateType<Reducer>): IResourcesViewProps => ({
    ...state,
    addModal: state.dashboard.resources.addModal,
    environmentsDataset: state.dashboard.resources.environments,
    filesDataset: state.dashboard.resources.files,
    repositoriesDataset: state.dashboard.resources.repositories,
  }
);

export const component: React.StatelessComponent<IResourcesViewProps> =
  (props: IResourcesViewProps): JSX.Element => {

        let onSubmitFunction: (((values: { resources: IResourcesViewProps["environmentsDataset"] }) => void)
         | ((values: { resources: IResourcesViewProps["repositoriesDataset"] }) => void)
         | ((values: { resources: IResourcesViewProps["filesDataset"] }) => void));
        if (props.addModal.type === "environment") {
         onSubmitFunction = (values: { resources: IResourcesViewProps["environmentsDataset"] }): void => {
          saveEnvs(values.resources, props.projectName, props.environmentsDataset);
        };
        } else if (props.addModal.type === "repository") {
         onSubmitFunction = (values: { resources: IResourcesViewProps["repositoriesDataset"] }): void => {
          saveRepos(values.resources, props.projectName, props.repositoriesDataset);
        };
        } else {
         onSubmitFunction = (values: { resources: IResourcesViewProps["filesDataset"] }): void => {
          saveFiles(values.resources, props.projectName, props.filesDataset);
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
                      onClick={(): void => { removeRepo(props.projectName); }}
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
                    dataset={props.repositoriesDataset}
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
                      },
                      {
                        dataField: "branch",
                        header: translate.t("search_findings.repositories_table.branch"),
                        isDate: false,
                        isStatus: false,
                        width: "30%",
                      },
                    ]}
                    id="tblRepositories"
                    pageSize={15}
                    title={translate.t("search_findings.tab_resources.repositories_title")}
                  />
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
                      onClick={(): void => { removeEnv(props.projectName); }}
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
                    dataset={props.environmentsDataset}
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
                      },
                    ]}
                    id="tblEnvironments"
                    pageSize={15}
                    title={translate.t("search_findings.tab_resources.environments_title")}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
        </Col>
      </Row>
      <hr/>
      {props.showFiles ?
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
                    <Col md={2} sm={6}>
                      <Button
                        id="downloadFile"
                        block={true}
                        bsStyle="primary"
                        onClick={(): void => {downloadFile(props.projectName); }}
                      >
                        <Glyphicon glyph="download-alt"/>&nbsp;
                        {translate.t("search_findings.tab_resources.download")}
                      </Button>
                    </Col>
                  </Col>
                </Row>
                <Row>
                  <Col md={12} sm={12}>
                    <DataTable
                      dataset={props.filesDataset}
                      onClickRow={(): void => {}}
                      enableRowSelection={true}
                      exportCsv={false}
                      search={true}
                      headers={[
                        {
                          dataField: "fileName",
                          header: translate.t("search_findings.files_table.file"),
                          isDate: false,
                          isStatus: false,
                          width: "25%",
                        },
                        {
                          dataField: "description",
                          header: translate.t("search_findings.files_table.description"),
                          isDate: false,
                          isStatus: false,
                          width: "50%",
                        },
                        {
                          dataField: "uploadDate",
                          header: translate.t("search_findings.files_table.upload_date"),
                          isDate: false,
                          isStatus: false,
                          width: "25%",
                        },
                      ]}
                      id="tblFiles"
                      pageSize={15}
                      title={translate.t("search_findings.tab_resources.files_title")}
                    />
                  </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
      : undefined}
      <AddResourcesModal
        isOpen={props.addModal.open}
        type={props.addModal.type}
        onClose={(): void => { store.dispatch(actions.closeAddModal()); }}
        onSubmit={onSubmitFunction}
      />
    </div>
  </React.StrictMode>
); };

export const resourcesView: ComponentType<IResourcesViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IResourcesViewProps>,
  mapStateToProps,
);
