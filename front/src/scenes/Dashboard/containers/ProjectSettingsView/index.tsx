/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Trans } from "react-i18next";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button/index";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { RemoveProjectModal } from "../../components/RemoveProjectModal";
import { IDashboardState } from "../../reducer";
import * as actions from "./actions";
import { Environments } from "./Environments";
import { Files } from "./Files";
import { Portfolio } from "./Portfolio";
import { GET_PROJECT_DATA } from "./queries";
import { Repositories } from "./Repositories";
import {
  IGetProjectData, IResourcesViewBaseProps, IResourcesViewDispatchProps, IResourcesViewProps,
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
      <Portfolio projectName={props.match.params.projectName} />
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
