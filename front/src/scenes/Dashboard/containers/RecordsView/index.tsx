/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { connect, ConnectedComponent, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import translate from "../../../../utils/translations/translate";
import { isValidEvidenceFile } from "../../../../utils/validations";
import { FileInput } from "../../components/FileInput/index";
import { IDashboardState } from "../../reducer";
import { removeRecords, ThunkDispatcher, updateRecords } from "./actions";
import { GET_FINDING_RECORDS } from "./queries";

type IRecordsViewBaseProps = Pick<RouteComponentProps<{ findingId: string }>, "match">;

type IRecordsViewStateProps = IDashboardState["records"] & { userRole: string };

interface IRecordsViewDispatchProps {
  onRemove(): void;
  onUpdate(): void;
}

type IRecordsViewProps = IRecordsViewBaseProps & (IRecordsViewStateProps & IRecordsViewDispatchProps);

const renderUploadField: ((arg1: IRecordsViewProps) => JSX.Element) = (props: IRecordsViewProps): JSX.Element => {
  const handleUpdateClick: (() => void) = (): void => {
    if (isValidEvidenceFile("#evidence8")) {
      mixpanel.track("UpdateRecords", {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
      props.onUpdate();
    }
  };

  return (
    <Row>
      <Col md={4} mdOffset={6} xs={12} sm={12}>
        <div>
          <FileInput
            icon="search"
            id="evidence8"
            type=".csv"
            visible={true}
          />
        </div>
      </Col>
      <Col sm={2}>
        <Button
          bsStyle="primary"
          block={true}
          onClick={handleUpdateClick}
        >
          <Glyphicon glyph="cloud-upload" />
          &nbsp;{translate.t("search_findings.tab_evidence.update")}
        </Button>
      </Col>
    </Row>
  );
};

const renderRemoveField: ((arg1: IRecordsViewProps) => JSX.Element) = (props: IRecordsViewProps): JSX.Element => {
  const handleRemoveClick: (() => void) = (): void => {
    mixpanel.track("RemoveRecords", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
    props.onRemove();
  };

  return (
    <Row>
      <Col md={4} mdOffset={6} xs={12} sm={12} />
      <Col sm={2}>
        <Button
          bsStyle="primary"
          block={true}
          onClick={handleRemoveClick}
        >
          <FluidIcon icon="delete" />
          &nbsp;{translate.t("search_findings.tab_evidence.remove")}
        </Button>
      </Col>
    </Row>
  );
};

export const recordsView: React.FC<IRecordsViewProps> = (props: IRecordsViewProps): JSX.Element => {
  const { findingId } = props.match.params;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingRecords", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_RECORDS} variables={{ findingId }}>
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }

          return (
            <React.Fragment>
              <Row>
                <Col md={2} mdOffset={10} xs={12} sm={12}>
                  <Button bsStyle="primary" block={true} onClick={handleEditClick}>
                    <FluidIcon icon="edit" />
                    &nbsp;{translate.t("search_findings.tab_evidence.editable")}
                  </Button>
                </Col>
              </Row>
              <br />
              {isEditing ? renderUploadField(props) : undefined}
              {isEditing && JSON.parse(data.finding.records).length > 0 ? renderRemoveField(props) : undefined}
              <Row>
                <DataTableNext
                  bordered={true}
                  dataset={JSON.parse(data.finding.records)}
                  exportCsv={false}
                  headers={[]}
                  id="tblRecords"
                  pageSize={15}
                  remote={false}
                  search={false}
                />
              </Row>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IRecordsViewStateProps, IRecordsViewBaseProps, IState> =
  (state: IState): IRecordsViewStateProps => ({
    ...state.dashboard.records,
    userRole: (window as Window & { userRole: string }).userRole,
  });

const mapDispatchToProps: MapDispatchToProps<IRecordsViewDispatchProps, IRecordsViewBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IRecordsViewBaseProps): IRecordsViewDispatchProps => {
    const { findingId } = ownProps.match.params;

    return ({
      onRemove: (): void => { dispatch(removeRecords(findingId)); },
      onUpdate: (): void => { dispatch(updateRecords(findingId)); },
    });
  };

const connectedRecordsView: ConnectedComponent<React.ComponentType<IRecordsViewProps>, IRecordsViewBaseProps> =
  connect(mapStateToProps, mapDispatchToProps)(recordsView);

export { connectedRecordsView as RecordsView };
