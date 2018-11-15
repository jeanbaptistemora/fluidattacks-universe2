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
import { Button, ButtonToolbar, Col, FormControl, Glyphicon, Grid, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { msgError } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import * as actions from "../../actions";

export interface IResourcesViewProps {
  addModal: {
    envFields: Array<{ environment: string }>;
    open: boolean;
    repoFields: Array<{ branch: string; repository: string }>;
    type: "repository" | "environment";
  };
  environmentsDataset: Array<{ urlEnv: string }>;
  projectName: string;
  repositoriesDataset: Array<{ branch: string; urlRepo: string }>;
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
  (arg1: IResourcesViewProps["addModal"]["repoFields"],
   arg2: IResourcesViewProps["projectName"],
   arg3: IResourcesViewProps["repositoriesDataset"],
  ) => void) =
  (reposData: IResourcesViewProps["addModal"]["repoFields"],
   projectName: IResourcesViewProps["projectName"],
   currentRepos: IResourcesViewProps["repositoriesDataset"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = reposData.filter(
      (newItem: IResourcesViewProps["addModal"]["repoFields"][0]) => _.findIndex(
        currentRepos,
        (currentItem: IResourcesViewProps["repositoriesDataset"][0]) =>
          currentItem.urlRepo === newItem.repository  && currentItem.branch === newItem.branch,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.saveRepos(projectName, reposData));
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
  (arg1: IResourcesViewProps["addModal"]["envFields"],
   arg2: IResourcesViewProps["projectName"],
   arg3: IResourcesViewProps["environmentsDataset"],
  ) => void) =
  (envsData: IResourcesViewProps["addModal"]["envFields"],
   projectName: IResourcesViewProps["projectName"],
   currentEnvs: IResourcesViewProps["environmentsDataset"],
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = envsData.filter(
    (newItem: IResourcesViewProps["addModal"]["envFields"][0]) => _.findIndex(
       currentEnvs,
       (currentItem: IResourcesViewProps["environmentsDataset"][0]) =>
          currentItem.urlEnv === newItem.environment,
    ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );
      thunkDispatch(actions.saveEnvs(projectName, envsData));
    }
};

const mapStateToProps: ((arg1: StateType<Reducer>) => IResourcesViewProps) =
  (state: StateType<Reducer>): IResourcesViewProps => ({
    ...state,
    addModal: state.dashboard.resources.addModal,
    environmentsDataset: state.dashboard.resources.environments,
    repositoriesDataset: state.dashboard.resources.repositories,
  });

export const component: React.StatelessComponent<IResourcesViewProps> =
  (props: IResourcesViewProps): JSX.Element => (
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
      <Modal
        open={props.addModal.open}
        onClose={(): void => {}}
        headerTitle={
          props.addModal.type === "environment"
          ? translate.t("search_findings.tab_resources.modal_env_title")
          : translate.t("search_findings.tab_resources.modal_repo_title")
        }
        content={
          <Grid>
            {
              props.addModal.type === "environment"
              ? <Row>
                {
                  props.addModal.envFields.map((field: { environment: string }, index: number) => (
                    <Row key={index}>
                      <Col md={7}>
                        <label>
                          <label style={{color: "#f22"}}>* </label>
                          {translate.t("search_findings.tab_resources.environment")}
                        </label>
                        <FormControl
                          id={`env: ${index}`}
                          componentClass="textarea"
                          value={field.environment}
                          required={true}
                          onChange={(evt: React.FormEvent<FormControl>): void => {
                            store.dispatch(actions.modifyEnvUrl(index, (evt.target as HTMLInputElement).value));
                          }}
                        />
                      </Col>
                      {
                        index > 0
                        ? <Col md={2} style={{ marginTop: "40px"}}>
                          <Button
                            bsStyle="primary"
                            onClick={(): void => { store.dispatch(actions.removeEnvironmentField(index)); }}
                          >
                            <Glyphicon glyph="trash"/>&nbsp;
                          </Button>
                        </Col>
                        : <Col/>
                      }
                    </Row>
                  ))}
                </Row>
              : <Row>
                {
                  props.addModal.repoFields.map((field: { branch: string; repository: string }, index: number) =>
                    (
                      <Row key={index}>
                        <Col md={5}>
                          <label>
                            <label style={{color: "#f22"}}>* </label>
                            {translate.t("search_findings.tab_resources.repository")}
                          </label>
                          <FormControl
                            id={`repo: ${index}`}
                            type="text"
                            value={field.repository}
                            required={true}
                            onChange={(evt: React.FormEvent<FormControl>): void => {
                              store.dispatch(actions.modifyRepoUrl(index, (evt.target as HTMLInputElement).value));
                            }}
                          />
                        </Col>
                        <Col md={2}>
                          <label>
                            <label style={{color: "#f22"}}>* </label>
                            {translate.t("search_findings.tab_resources.branch")}
                          </label>
                          <FormControl
                            id={`branch: ${index}`}
                            type="text"
                            value={field.branch}
                            required={true}
                            onChange={(evt: React.FormEvent<FormControl>): void => {
                              store.dispatch(actions.modifyRepoBranch(index, (evt.target as HTMLInputElement).value));
                            }}
                          />
                        </Col>
                        {
                          index > 0
                          ? <Col md={2} style={{ marginTop: "40px"}}>
                            <Button
                              bsStyle="primary"
                              onClick={(): void => { store.dispatch(actions.removeRepositoryField(index)); }}
                            >
                              <Glyphicon glyph="trash"/>&nbsp;
                            </Button>
                          </Col>
                          : <Col/>
                        }
                      </Row>
                  ))}
                </Row>
            }
            <br/>
            <Button
              bsStyle="primary"
              onClick={
                props.addModal.type === "environment"
                ? (): void => { store.dispatch(actions.addEnvironmentField()); }
                : (): void => { store.dispatch(actions.addRepositoryField()); }
              }
            >
              <Glyphicon glyph="plus"/>
            </Button>
          </Grid>
        }
        footer={
          <Row>
            <ButtonToolbar className="pull-right">
              <Button
                bsStyle="default"
                onClick={(): void => { store.dispatch(actions.closeAddModal()); }}
              >
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button
                bsStyle="primary"
                onClick={
                  props.addModal.type === "environment"
                  ? (): void => { saveEnvs(
                      props.addModal.envFields,
                      props.projectName,
                      props.environmentsDataset,
                     );
                   }
                  : (): void => { saveRepos(
                      props.addModal.repoFields,
                      props.projectName,
                      props.repositoriesDataset,
                     );
                   }
                }
              >
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </Row>
        }
      />
    </div>
  </React.StrictMode>
);

export const resourcesView: ComponentType<IResourcesViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IResourcesViewProps>,
  mapStateToProps,
);
