/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { Button } from "../../../../../components/Button";
import { ConfirmDialog, ConfirmFn } from "../../../../../components/ConfirmDialog";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { changeFormatter, statusFormatter } from "../../../../../components/DataTableNext/formatters";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import translate from "../../../../../utils/translations/translate";
import { addRepositoriesModal as AddRepositoriesModal } from "../../../components/AddRepositoriesModal/index";
import { ADD_RESOURCE_MUTATION, GET_REPOSITORIES, UPDATE_RESOURCE_MUTATION } from "../queries";
import { IHistoricState, IRepositoriesAttr } from "../types";

interface IRepositoriesProps {
  projectName: string;
}

const repositories: React.FC<IRepositoriesProps> = (props: IRepositoriesProps): JSX.Element => {
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [filterValue, setFilterValue] = React.useState("");
  const [sortValue, setSortValue] = React.useState({});

  // GraphQL operations
  const { data, refetch } = useQuery(GET_REPOSITORIES, { variables: { projectName: props.projectName } });
  const [addRepositories] = useMutation(ADD_RESOURCE_MUTATION, { onCompleted: refetch });
  const [updateRepositories] = useMutation(UPDATE_RESOURCE_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectRepo", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_change"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const reposDataset: IRepositoriesAttr[] = JSON.parse(data.resources.repositories)
    .map((repo: IRepositoriesAttr) => {
      const historicState: IHistoricState[] = _.get(repo, "historic_state", [{ date: "", state: "ACTIVE", user: "" }]);

      return {
        ...repo,
        state: _.capitalize((_.last(historicState) as IHistoricState).state),
      };
    });

  const isRepeated: ((newRepo: IRepositoriesAttr) => boolean) = (newRepo: IRepositoriesAttr): boolean => {
    const repeatedItems: IRepositoriesAttr[] = reposDataset.filter((repo: IRepositoriesAttr): boolean =>
      repo.branch === newRepo.branch
      && repo.urlRepo === newRepo.urlRepo
      && repo.protocol === newRepo.protocol);

    return repeatedItems.length > 0;
  };

  const handleRepoAdd: ((values: { resources: IRepositoriesAttr[] }) => void) = (
    values: { resources: IRepositoriesAttr[] },
  ): void => {
    const containsRepeated: boolean = values.resources.filter(isRepeated).length > 0;

    if (containsRepeated) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      closeAddModal();
      addRepositories({
        variables: {
          projectName: props.projectName,
          resData: JSON.stringify(values.resources),
          resType: "repository",
        },
      })
        .catch();
    }
  };

  return (
    <React.StrictMode>
      <Row>
        <Col md={11}>
          <h3>{translate.t("search_findings.tab_resources.repositories_title")}</h3>
        </Col>
        {userRole === "customer" ? (
          <Col md={1}>
            <Button block={true} onClick={openAddModal}>
              <Glyphicon glyph="plus" />&nbsp;
              {translate.t("search_findings.tab_resources.add_repository")}
            </Button>
          </Col>
        ) : undefined}
      </Row>
      <ConfirmDialog title="Change repository state">
        {(confirm: ConfirmFn): React.ReactNode => {
          const handleStateUpdate: ((repo: Dictionary<string>) => void) = (repo: Dictionary<string>): void => {
            confirm(() => {
              updateRepositories({
                variables: {
                  projectName: props.projectName,
                  resData: JSON.stringify({
                    ...repo,
                    state: repo.state === "Active" ? "INACTIVE" : "ACTIVE",
                  }),
                  resType: "repository",
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
              dataField: "protocol",
              header: translate.t("search_findings.repositories_table.protocol"),
              onSort: sortState,
              width: "14%",
              wrapped: true,
            },
            {
              dataField: "urlRepo",
              header: translate.t("search_findings.repositories_table.repository"),
              onSort: sortState,
              width: "56%",
              wrapped: true,
            },
            {
              dataField: "branch",
              header: translate.t("search_findings.repositories_table.branch"),
              onSort: sortState,
              width: "18%",
              wrapped: true,
            },
            {
              align: "center",
              changeFunction: handleStateUpdate,
              dataField: "state",
              filter: filterState,
              formatter: userRole === "customer" ? changeFormatter : statusFormatter,
              header: translate.t("search_findings.repositories_table.state"),
              onSort: sortState,
              width: "12%",
              wrapped: true,
            },
          ];

          return (
            <DataTableNext
              bordered={true}
              dataset={reposDataset}
              defaultSorted={sortValue}
              exportCsv={true}
              search={true}
              headers={tableHeaders}
              id="tblRepositories"
              pageSize={15}
              remote={false}
              striped={true}
            />
          );
        }}
      </ConfirmDialog>
      <label>
        <b>{translate.t("search_findings.tab_resources.total_repos")}</b>{reposDataset.length}
      </label>
      <AddRepositoriesModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleRepoAdd} />
    </React.StrictMode>
  );
};

export { repositories as Repositories };
