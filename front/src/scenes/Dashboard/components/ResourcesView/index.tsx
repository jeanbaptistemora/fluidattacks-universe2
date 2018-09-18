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
import React, { ComponentType } from "react";
import { Button, ButtonToolbar, Col, FormControl, Glyphicon, Grid, Row } from "react-bootstrap";
import {
  InferableComponentEnhancer,
  lifecycle,
} from "recompose";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import { default as DataTable } from "../../../../components/DataTable/index";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";

declare var $: any;

interface IResourcesViewProps {
  addModal: {
    fields: Array<{ branch: string; repository: string }>;
    open: boolean;
  };
  projectName: string;
  repositoriesDataset: string[];
  translations: { [key: string]: string };
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle({
  componentDidMount(): void {
    const { projectName }: any = this.props;
    let gQry: string;
    gQry = `{
        resources (projectName: "${projectName}") {
          repositories,
          access
        }
    }`;
    new Xhr().request(gQry, "An error occurred getting repositories")
    .then((resp: AxiosResponse) => {
      store.dispatch(actions.loadResources(
        JSON.parse(resp.data.data.resources.repositories),
      ));
    })
    .catch((error: string) => {
      rollbar.error(error);
    });
  },
});

const removeRepo: ((arg1: IResourcesViewProps) => void) =
  (props: IResourcesViewProps): void => {
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
          projectName: "${props.projectName}"
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
        store.dispatch(actions.loadResources(
          JSON.parse(resp.data.data.removeRepositories.resources.repositories),
        ));
      })
      .catch((error: string) => {
        rollbar.error(`An error occurred removing repositories: ${error}`);
      });
    } else {
      rollbar.error("An error occurred removing repositories");
    }
  } else {
    $.gritter.add({
      class_name: "color danger",
      sticky: false,
      text: props.translations["search_findings.tab_resources.no_selection"],
      title: "Oops!",
    });
  }
};

const saveRepos: ((arg1: Array<{ branch: string; repository: string }>, arg2: string) => void) =
  (reposData: Array<{ branch: string; repository: string }>, projectName: string): void => {
    let gQry: string;
    gQry = `mutation {
      addRepositories (
        resourcesData: ${JSON.stringify(JSON.stringify(reposData))},
        projectName: "${projectName}") {
        success,
        access,
        resources {
          repositories
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred adding repositories")
    .then((resp: AxiosResponse) => {
      store.dispatch(actions.closeAddModal());
      store.dispatch(actions.loadResources(
        JSON.parse(resp.data.data.addRepositories.resources.repositories),
      ));
    })
    .catch((error: string) => {
      rollbar.error(error);
    });
};

const mapStateToProps: ((arg1: StateType<Reducer>) => IResourcesViewProps) =
  (state: StateType<Reducer>): IResourcesViewProps => ({
    ...state,
    addModal: state.dashboard.resources.addModal,
    repositoriesDataset: state.dashboard.resources.repositories,
  });

const component: React.StatelessComponent<IResourcesViewProps> =
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
                      id="remove"
                      block={true}
                      bsStyle="primary"
                      onClick={(): void => { removeRepo(props); }}
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
      <Modal
        open={props.addModal.open}
        onClose={(): void => {}}
        headerTitle={
          props.translations["search_findings.tab_resources.title_repo"]
        }
        content={
          <Grid>
              <Row>
                {
                  props.addModal.fields.map((field: { branch: string; repository: string }, index: number) =>
                    (
                      <Row>
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
            <br/>
            <Button
              bsStyle="primary"
              onClick={(): void => { store.dispatch(actions.addRepositoryField()); }}
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
                onClick={(): void => { saveRepos(props.addModal.fields, props.projectName); }}
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
