/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { Button } from "../../../../../components/Button";
import { ConfirmDialog, ConfirmFn } from "../../../../../components/ConfirmDialog";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { changeFormatter, statusFormatter } from "../../../../../components/DataTableNext/formatters";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import translate from "../../../../../utils/translations/translate";
import { AddEnvironmentsModal } from "../../../components/AddEnvironmentsModal/index";
import { ADD_RESOURCE_MUTATION, GET_ENVIRONMENTS, UPDATE_RESOURCE_MUTATION } from "../queries";
import { IEnvironmentsAttr, IHistoricState } from "../types";

interface IEnvironmentsProps {
  projectName: string;
}

const environments: React.FC<IEnvironmentsProps> = (props: IEnvironmentsProps): JSX.Element => {
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [filterValue, setFilterValue] = React.useState("");
  const [sortValue, setSortValue] = React.useState({});

  // GraphQL operations
  const { data, refetch } = useQuery(GET_ENVIRONMENTS, { variables: { projectName: props.projectName } });
  const [addEnvironments] = useMutation(ADD_RESOURCE_MUTATION, { onCompleted: refetch });
  const [updateEnvironments] = useMutation(UPDATE_RESOURCE_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectEnv", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_change"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const envsDataset: IEnvironmentsAttr[] = JSON.parse(data.resources.environments)
    .map((env: IEnvironmentsAttr) => {
      const historicState: IHistoricState[] = _.get(env, "historic_state", [{ date: "", state: "ACTIVE", user: "" }]);

      return {
        ...env,
        state: _.capitalize((_.last(historicState) as IHistoricState).state),
      };
    });

  const isRepeated: ((newEnv: IEnvironmentsAttr) => boolean) = (newEnv: IEnvironmentsAttr): boolean => {
    const repeatedItems: IEnvironmentsAttr[] = envsDataset.filter((env: IEnvironmentsAttr): boolean =>
      env.urlEnv === newEnv.urlEnv);

    return repeatedItems.length > 0;
  };

  const handleEnvAdd: ((values: { resources: IEnvironmentsAttr[] }) => void) = (
    values: { resources: IEnvironmentsAttr[] },
  ): void => {
    const containsRepeated: boolean = values.resources.filter(isRepeated).length > 0;

    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      closeAddModal();
      addEnvironments({
        variables: {
          projectName: props.projectName,
          resData: JSON.stringify(values.resources),
          resType: "environment",
        },
      })
        .catch();
    }
  };

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.tab_resources.environments_title")}</h3>
        </Col>
        {_.includes(["admin", "customer"], userRole) ? (
          <Col lg={4} md={2} xs={5}>
            <ButtonToolbar className="pull-right">
              <Button block={true} onClick={openAddModal}>
                <Glyphicon glyph="plus" />&nbsp;
              {translate.t("search_findings.tab_resources.add_repository")}
              </Button>
            </ButtonToolbar>
          </Col>
        ) : undefined}
      </Row>
      <ConfirmDialog title="Change environment state">
        {(confirm: ConfirmFn): React.ReactNode => {
          const handleStateUpdate: ((env: Dictionary<string>) => void) = (env: Dictionary<string>): void => {
            confirm(() => {
              updateEnvironments({
                variables: {
                  projectName: props.projectName,
                  resData: JSON.stringify({
                    ...env,
                    state: env.state === "Active" ? "INACTIVE" : "ACTIVE",
                  }),
                  resType: "environment",
                },
              })
                .catch();
            });
          };

          const sortState: ((dataField: string, order: SortOrder) => void) = (
            dataField: string, order: SortOrder,
          ): void => {
            const newSorted: Sorted = { dataField, order };
            setSortValue(newSorted);
          };

          const filterState: {} = selectFilter({
            defaultValue: filterValue,
            onFilter: (filterVal: string): void => {
              setFilterValue(filterVal);
            },
            options: [
              { value: "Active", label: "Active" },
              { value: "Inactive", label: "Inactive" },
            ],
          });

          const tableHeaders: IHeader[] = [
            {
              dataField: "urlEnv",
              header: translate.t("search_findings.environment_table.environment"),
              onSort: sortState,
              wrapped: true,
            },
            {
              align: "center",
              changeFunction: handleStateUpdate,
              dataField: "state",
              filter: filterState,
              formatter: _.includes(["admin", "customer"], userRole) ? changeFormatter : statusFormatter,
              header: translate.t("search_findings.repositories_table.state"),
              onSort: sortState,
              width: "12%",
              wrapped: true,
            },
          ];

          return (
            <DataTableNext
              bordered={true}
              dataset={envsDataset}
              defaultSorted={sortValue}
              exportCsv={true}
              search={true}
              headers={tableHeaders}
              id="tblEnvironments"
              pageSize={15}
              remote={false}
              striped={true}
            />
          );
        }}
      </ConfirmDialog>
      <label>
        <b>{translate.t("search_findings.tab_resources.total_envs")}</b>{envsDataset.length}
      </label>
      <AddEnvironmentsModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleEnvAdd} />
    </React.StrictMode>
  );
};

export { environments as Environments };
