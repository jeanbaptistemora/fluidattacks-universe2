/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext";
import { default as globalStyle } from "../../../../styles/global.css";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { addTagsModal as AddTagsModal } from "../../components/AddTagsModal/index";
import { RemoveProjectModal } from "../../components/RemoveProjectModal";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import { Environments } from "./Environments";
import { Files } from "./Files";
import {
  ADD_TAGS_MUTATION, GET_PROJECT_DATA, GET_TAGS, REMOVE_TAG_MUTATION,
} from "./queries";
import { Repositories } from "./Repositories";
import {
  IAddTagsAttr, IGetProjectData, IProjectTagsAttr, IRemoveTagsAttr,
  IResourcesViewBaseProps, IResourcesViewDispatchProps, IResourcesViewProps,
  IResourcesViewStateProps,
} from "./types";

const enhance: InferableComponentEnhancer<{}> = lifecycle<IResourcesViewProps, {}>({
  componentDidMount(): void {
    mixpanel.track(
      "ProjectResources",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
  },
});

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

const allowedRoles: string[] = ["customer"];

const renderTagsView: ((props: IResourcesViewProps) => JSX.Element) = (props: IResourcesViewProps): JSX.Element => {
  const { userRole: currUserRole } = (window as typeof window & Dictionary<string>);
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
        ({ error, data, refetch }: QueryResult<IProjectTagsAttr>): JSX.Element => {
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
                      {(removeTag: MutationFunction, mutationRes: MutationResult): JSX.Element => {
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
                  {(addTags: MutationFunction, mutationRes: MutationResult): JSX.Element => {
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
          } else { return <React.Fragment />; }
        }}
    </Query>
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
      ({ data }: QueryResult<IGetProjectData>): JSX.Element => {
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
        } else { return <React.Fragment />; }
      }}
    </Query>

  );
};

const projectResourcesView: React.FunctionComponent<IResourcesViewProps> =
  (props: IResourcesViewProps): JSX.Element =>
  (
  <React.StrictMode>
    <div id="resources" className="tab-pane cont active">
      <Repositories projectName={props.match.params.projectName} />
      <Environments projectName={props.match.params.projectName} />
      <Files projectName={props.match.params.projectName} />
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
    tagsModal: state.dashboard.tags.tagsModal,
  });

const mapDispatchToProps: MapDispatchToProps<IResourcesViewDispatchProps, IResourcesViewBaseProps> =
  (dispatch: actions.ThunkDispatcher): IResourcesViewDispatchProps => ({
      onCloseTagsModal: (): void => { dispatch(actions.closeTagsModal()); },
      onOpenTagsModal: (): void => { dispatch(actions.openTagsModal()); },
      onSort: (newValues: {}): void => {dispatch(actions.changeSortedValues(newValues)); },
    });

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectResourcesView));
