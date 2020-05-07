/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
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
import { Can } from "../../../../../utils/authz/Can";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { AddRepositoriesModal } from "../../../components/AddRepositoriesModal/index";
import { ADD_REPOSITORIES_MUTATION, GET_REPOSITORIES, UPDATE_REPOSITORY_MUTATION } from "../queries";
import { IHistoricState, IRepositoriesAttr } from "../types";

interface IRepositoriesProps {
  projectName: string;
}

const repositories: React.FC<IRepositoriesProps> = (props: IRepositoriesProps): JSX.Element => {
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  // GraphQL operations
  const { data, refetch } = useQuery(GET_REPOSITORIES, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred loading project repos", error);
    },
    variables: { projectName: props.projectName },
  });
  const [addRepositories] = useMutation(ADD_REPOSITORIES_MUTATION, {
    onCompleted: refetch,
    onError: (reposError: ApolloError): void => {
      reposError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - One or more values already exist":
            msgError(translate.t("search_findings.tab_resources.repeated_item"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding repositories", reposError);
        }
      });
    },
  });
  const [updateRepository] = useMutation(UPDATE_REPOSITORY_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectRepo", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_change"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred updating repository state", error);
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

  const handleRepoAdd: ((values: { resources: IRepositoriesAttr[] }) => void) = (
    values: { resources: IRepositoriesAttr[] },
  ): void => {
    const repeatedInputs: IRepositoriesAttr[] = values.resources.filter((repo: IRepositoriesAttr) =>
      values.resources.filter(_.matches(repo)).length > 1);
    const repeatedRepos: IRepositoriesAttr[] = values.resources.filter((repo: IRepositoriesAttr) =>
      reposDataset.filter(_.matches(repo)).length > 0);

    if (repeatedInputs.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_input"));
    } else if (repeatedRepos.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      closeAddModal();
      addRepositories({
        variables: {
          projectName: props.projectName,
          repos: values.resources,
        },
      })
        .catch();
    }
  };

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.tab_resources.repositories_title")}</h3>
        </Col>
        <Can do="backend_api_resolvers_resource__do_add_repositories">
          <Col lg={4} md={2} xs={5}>
            <ButtonToolbar className="pull-right">
              <Button onClick={openAddModal}>
                <Glyphicon glyph="plus" />&nbsp;
              {translate.t("search_findings.tab_resources.add_repository")}
              </Button>
            </ButtonToolbar>
          </Col>
        </Can>
      </Row>
      <Can do="backend_api_resolvers_resource__do_update_repository" passThrough={true}>
        {(canUpdate: boolean): JSX.Element => (
      <ConfirmDialog title="Change repository state">
        {(confirm: ConfirmFn): React.ReactNode => {
          const handleStateUpdate: ((repo: Dictionary<string>) => void) = (repo: Dictionary<string>): void => {
            confirm(() => {
              updateRepository({
                variables: {
                  projectName: props.projectName,
                  repo: {
                    branch: repo.branch,
                    protocol: _.isNil(repo.protocol) ? "" : repo.protocol,
                    urlRepo: repo.urlRepo,
                  },
                  state: repo.state === "Active" ? "INACTIVE" : "ACTIVE",
                },
              })
                .catch();
            });
          };

          const sortState: ((dataField: string, order: SortOrder) => void) = (
            dataField: string, order: SortOrder,
          ): void => {
            const newSorted: Sorted = { dataField, order };
            sessionStorage.setItem("repoSort", JSON.stringify(newSorted));
          };

          const filterState: {} = selectFilter({
            defaultValue: _.get(sessionStorage, "repoStateFilter"),
            onFilter: (filterVal: string): void => {
              sessionStorage.setItem("repoStateFilter", filterVal);
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
              formatter: canUpdate ? changeFormatter : statusFormatter,
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
              defaultSorted={JSON.parse(_.get(sessionStorage, "repoSort", "{}"))}
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
        )}
      </Can>
      <label>
        <b>{translate.t("search_findings.tab_resources.total_repos")}</b>{reposDataset.length}
      </label>
      <AddRepositoriesModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleRepoAdd} />
    </React.StrictMode>
  );
};

export { repositories as Repositories };
