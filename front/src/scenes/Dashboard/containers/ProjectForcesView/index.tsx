/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import _ from "lodash";
import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { RouteComponentProps } from "react-router";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";
import { Dispatch } from "redux";

// Local imports
import { Button } from "../../../../components/Button";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { changeSortValues } from "./actions";
import { GET_FORCES_EXECUTIONS } from "./queries";

type ForcesViewProps = RouteComponentProps<{ projectName: string }>;

const projectForcesView: React.FunctionComponent<ForcesViewProps> = (props: ForcesViewProps): JSX.Element => {

  interface IState { dashboard: IDashboardState; }
  const forces: IDashboardState["forces"] = useSelector(
    (state: IState): IDashboardState["forces"] => state.dashboard.forces);

  // States
  const [currentRowIndex, updateRowIndex] = React.useState(0);
  const [sortValue, setSortValue] = React.useState(forces.defaultSort);
  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] = React.useState(false);

  const dispatch: Dispatch = useDispatch();

  const onSortState: ((dataField: string, order: SortOrder) => void) =
  (dataField: string, order: SortOrder): void => {
    const newSorted: Sorted = {dataField,  order};
    if (!_.isEqual(newSorted, sortValue)) {
      setSortValue(newSorted);
      dispatch(changeSortValues(newSorted));
    }
  };

  const tableHeaders: IHeader[] = [
    {
      align: "center", dataField: "date", header: translate.t("project.forces.date"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "strictness", header: translate.t("project.forces.strictness"),
      onSort: onSortState, width: "5%", wrapped: true,
    },
    {
      align: "center", dataField: "kind", header: translate.t("project.forces.kind"),
      onSort: onSortState, width: "5%", wrapped: true,
    },
    {
      align: "center", dataField: "gitRepo", header: translate.t("project.forces.git_repo"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "identifier", header: translate.t("project.forces.identifier"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
  ];
  const { projectName } = props.match.params;

  const openSeeExecutionDetailsModal: ((event: object, row: object, rowIndex: number) => void) =
  (event: object, row: object, rowIndex: number): void => {
    updateRowIndex(rowIndex);
    setExecutionDetailsModalOpen(true);
  };

  const closeSeeExecutionDetailsModal: (() => void) = (): void => {
    setExecutionDetailsModalOpen(false);
  };

  return (
    <Query
      query={GET_FORCES_EXECUTIONS}
      variables={{ projectName }}
    >
      {
        ({ data, error, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {
            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting executions", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            return (
              <React.StrictMode>
                <p>{translate.t("project.forces.table_advice")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={data.breakBuildExecutions.executions}
                  defaultSorted={sortValue}
                  exportCsv={true}
                  search={true}
                  headers={tableHeaders}
                  id="tblForcesExecutions"
                  pageSize={100}
                  remote={false}
                  rowEvents={{onClick: openSeeExecutionDetailsModal}}
                  title=""
                />
              <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.forces.execution_details_modal.title")}
                  open={isExecutionDetailsModalOpen}
              >
                <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
                  {currentRowIndex >= 0 && currentRowIndex < data.breakBuildExecutions.executions.length
                    ? data.breakBuildExecutions.executions[currentRowIndex].log
                    : "Unable to retrieve"}
                </SyntaxHighlighter>
                <ButtonToolbar className="pull-right">
                  <Button bsStyle="success" onClick={closeSeeExecutionDetailsModal}>
                    {translate.t("project.forces.execution_details_modal.close")}
                  </Button>
                </ButtonToolbar>
              </Modal>
              </React.StrictMode>
            );
          } else {
            return <React.Fragment />;
          }
        }}
    </Query>
  );
};

export { projectForcesView as ProjectForcesView };
