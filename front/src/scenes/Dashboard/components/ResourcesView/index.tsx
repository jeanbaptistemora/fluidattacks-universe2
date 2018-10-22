/* tslint:disable:jsx-no-lambda no-any jsx-no-multiline-js no-empty
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 *
 * NO-ANY: Disabling this rule is necessary because there are no specific types
 * for functions such as mapStateToProps and mapDispatchToProps used in the
 * redux wrapper of this component
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { AxiosResponse } from "axios";
import _ from "lodash";
import React, { ComponentType } from "react";
import { Button, ButtonToolbar, Col, FormControl, Glyphicon, Grid, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import { dataTable as DataTable } from "../../../../components/DataTable/index";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";

interface IResourcesViewProps {
  addModal: {
    envFields: Array<{ environment: string }>;
    open: boolean;
    repoFields: Array<{ branch: string; repository: string }>;
    type: "repository" | "environment";
  };
  environmentsDataset: Array<{ urlEnv: string }>;
  projectName: string;
  repositoriesDataset: Array<{ branch: string; urlRepo: string }>;
  translations: { [key: string]: string };
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    store.dispatch(actions.clearResources());
    const { projectName, translations }: any = this.props;
    let gQry: string;
    gQry = `{
        resources (projectName: "${projectName}") {
          environments
          repositories
        }
    }`;
    new Xhr().request(gQry, "An error occurred getting repositories")
    .then((response: AxiosResponse) => {
      const { data, errors } = response.data;
      if (_.isNil(data)) {
        location.reload();
      } else {
        if (errors) {
          const { message } = errors[0];
          if (_.includes(["Login required", "Invalid token"], message)) {
            location.assign("/logout");
          } else if (message === "Access denied") {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          store.dispatch(actions.loadResources(
            JSON.parse(data.resources.repositories),
            JSON.parse(data.resources.environments),
          ));
        }
      }
    })
    .catch((error: string) => {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error(error);
    });
  },
});

const removeRepo: ((arg1: { [key: string]: string }, arg2: string) => void) =
  (translations: { [key: string]: string }, projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblRepositories tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const repository: string | null = selectedRow.children[1].textContent;
      const branch: string | null = selectedRow.children[2].textContent;

      let gQry: string;
      gQry = `mutation {
        removeRepositories (
          repositoryData: ${JSON.stringify(JSON.stringify({ urlRepo: repository, branch}))},
          projectName: "${projectName}"
        ) {
          success,
          access,
          resources {
            repositories
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred removing repositories")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error && resp.data.data.removeRepositories.success) {
          if (resp.data.data.removeRepositories.access) {
            store.dispatch(actions.loadResources(
              JSON.parse(resp.data.data.removeRepositories.resources.repositories),
            ));
            msgSuccess(
              translations["search_findings.tab_resources.success_remove"],
              translations["search_findings.tab_users.title_success"],
            );
          } else {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error("An error occurred removing repositories");
        }
      })
      .catch((error: string) => {
        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(`An error occurred removing repositories: ${error}`);
      });
    } else {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error("An error occurred removing repositories");
    }
  } else {
    msgError(translations["search_findings.tab_resources.no_selection"]);
  }
};

const saveRepos: (
  (arg1: Array<{ branch: string; repository: string }>,
   arg2: string,
   arg3: { [key: string]: string },
   arg4: Array<{ branch: string; urlRepo: string }>,
  ) => void) =
  (reposData: Array<{ branch: string; repository: string }>,
   projectName: string,
   translations: { [key: string]: string },
   currentRepos: Array<{ branch: string; urlRepo: string }>,
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = reposData.filter(
      (newItem: { branch: string; repository: string }) => _.findIndex(
        currentRepos,
        (currentItem: { branch: string; urlRepo: string }) =>
          currentItem.urlRepo === newItem.repository  && currentItem.branch === newItem.branch,
      ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translations["search_findings.tab_resources.repeated_item"]);
    } else {
      let gQry: string;
      gQry = `mutation {
        addRepositories (
          resourcesData: ${JSON.stringify(JSON.stringify(reposData))},
          projectName: "${projectName}") {
          success,
          access,
          resources {
            environments,
            repositories
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred adding repositories")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error && resp.data.data.addRepositories.success) {
          if (resp.data.data.addRepositories.access) {
            store.dispatch(actions.closeAddModal());
            store.dispatch(actions.loadResources(
              JSON.parse(resp.data.data.addRepositories.resources.repositories),
              JSON.parse(resp.data.data.addRepositories.resources.environments),
            ));
            msgSuccess(
              translations["search_findings.tab_resources.success"],
              translations["search_findings.tab_users.title_success"],
            );
          } else {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error("An error occurred adding repositories");
        }
      })
      .catch((error: string) => {
        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(error);
      });
    }
};

const removeEnv: ((arg1: { [key: string]: string }, arg2: string) => void) =
  (translations: { [key: string]: string }, projectName: string): void => {
  const selectedQry: NodeListOf<Element> = document.querySelectorAll("#tblEnvironments tr input:checked");
  if (selectedQry.length > 0) {
    if (selectedQry[0].closest("tr") !== null) {
      const selectedRow: Element = selectedQry[0].closest("tr") as Element;
      const env: string | null = selectedRow.children[1].textContent;

      let gQry: string;
      gQry = `mutation {
        removeEnvironments (
          repositoryData: ${JSON.stringify(JSON.stringify({ urlEnv: env}))},
          projectName: "${projectName}"
        ) {
          success,
          access,
          resources {
            environments,
            repositories
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred removing environments")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error && resp.data.data.removeEnvironments.success) {
          if (resp.data.data.removeEnvironments.access) {
            store.dispatch(actions.loadResources(
              JSON.parse(resp.data.data.removeEnvironments.resources.repositories),
              JSON.parse(resp.data.data.removeEnvironments.resources.environments),
            ));
            msgSuccess(
              translations["search_findings.tab_resources.success_remove"],
              translations["search_findings.tab_users.title_success"],
            );
          } else {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error("An error occurred removing environments");
        }
      })
      .catch((error: string) => {
        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(`An error occurred removing environments: ${error}`);
      });
    } else {
      msgError(translations["proj_alerts.error_textsad"]);
      rollbar.error("An error occurred removing environments");
    }
  } else {
    msgError(translations["search_findings.tab_resources.no_selection"]);
  }
};

const saveEnvs: (
  (arg1: Array<{ environment: string }>,
   arg2: string,
   arg3: { [key: string]: string },
   arg4: Array<{ urlEnv: string }>,
  ) => void) =
  (envsData: Array<{ environment: string }>,
   projectName: string,
   translations: { [key: string]: string },
   currentEnvs: Array<{ urlEnv: string }>,
  ): void => {
    let containsRepeated: boolean;
    containsRepeated = envsData.filter(
    (newItem: { environment: string }) => _.findIndex(
       currentEnvs,
       (currentItem: { urlEnv: string }) => currentItem.urlEnv === newItem.environment,
    ) > -1).length > 0;
    if (containsRepeated) {
      msgError(translations["search_findings.tab_resources.repeated_item"]);
    } else {
      let gQry: string;
      gQry = `mutation {
        addEnvironments (
          resourcesData: ${JSON.stringify(JSON.stringify(envsData))},
          projectName: "${projectName}") {
          success,
          access,
          resources {
            environments,
            repositories
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred adding environments")
      .then((resp: AxiosResponse) => {
        if (!resp.data.error && resp.data.data.addEnvironments.success) {
          if (resp.data.data.addEnvironments.access) {
            store.dispatch(actions.closeAddModal());
            store.dispatch(actions.loadResources(
              JSON.parse(resp.data.data.addEnvironments.resources.repositories),
              JSON.parse(resp.data.data.addEnvironments.resources.environments),
            ));
            msgSuccess(
              translations["search_findings.tab_resources.success"],
              translations["search_findings.tab_users.title_success"],
            );
          } else {
            msgError(translations["proj_alerts.access_denied"]);
          }
        } else {
          msgError(translations["proj_alerts.error_textsad"]);
          rollbar.error("An error occurred adding repositories");
        }
      })
      .catch((error: string) => {
        msgError(translations["proj_alerts.error_textsad"]);
        rollbar.error(error);
      });
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
                      {props.translations["search_findings.tab_resources.add_repository"]}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button
                      id="removeRepository"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeRepo(props.translations, props.projectName); }}
                    >
                      <Glyphicon glyph="minus"/>&nbsp;
                      {props.translations["search_findings.tab_resources.remove_repository"]}
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
                        header: props.translations["search_findings.repositories_table.repository"],
                        isDate: false,
                        isStatus: false,
                        width: "70%",
                      },
                      {
                        dataField: "branch",
                        header: props.translations["search_findings.repositories_table.branch"],
                        isDate: false,
                        isStatus: false,
                        width: "30%",
                      },
                    ]}
                    id="tblRepositories"
                    pageSize={15}
                    title={props.translations["search_findings.tab_resources.repositories"]}
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
                      {props.translations["search_findings.tab_resources.add_repository"]}
                    </Button>
                  </Col>
                  <Col md={2} sm={6}>
                    <Button
                      id="removeEnvironment"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeEnv(props.translations, props.projectName); }}
                    >
                      <Glyphicon glyph="minus"/>&nbsp;
                      {props.translations["search_findings.tab_resources.remove_repository"]}
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
                        header: props.translations["search_findings.environment_table.environment"],
                        isDate: false,
                        isStatus: false,
                      },
                    ]}
                    id="tblEnvironments"
                    pageSize={15}
                    title={props.translations["search_findings.tab_resources.environments"]}
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
          ? props.translations["search_findings.tab_resources.title_env"]
          : props.translations["search_findings.tab_resources.title_repo"]
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
                          {props.translations["search_findings.tab_resources.environment"]}
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
                            {props.translations["search_findings.tab_resources.repository"]}
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
                            {props.translations["search_findings.tab_resources.branch"]}
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
                {props.translations["confirmmodal.cancel"]}
              </Button>
              <Button
                bsStyle="primary"
                onClick={
                  props.addModal.type === "environment"
                  ? (): void => { saveEnvs(
                      props.addModal.envFields,
                      props.projectName, props.translations,
                      props.environmentsDataset,
                     );
                   }
                  : (): void => { saveRepos(
                      props.addModal.repoFields,
                      props.projectName,
                      props.translations,
                      props.repositoriesDataset,
                     );
                   }
                }
              >
                {props.translations["confirmmodal.proceed"]}
              </Button>
            </ButtonToolbar>
          </Row>
        }
      />
    </div>
  </React.StrictMode>
);

component.defaultProps = {
  translations: {},
};

export const resourcesView: ComponentType<IResourcesViewProps> = reduxWrapper
(
  enhance(component) as React.StatelessComponent<IResourcesViewProps>,
  mapStateToProps,
);
