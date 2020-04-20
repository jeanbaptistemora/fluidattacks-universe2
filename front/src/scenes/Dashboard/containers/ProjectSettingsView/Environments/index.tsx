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
import { AddEnvironmentsModal } from "../../../components/AddEnvironmentsModal/index";
import { ADD_ENVIRONMENTS_MUTATION, GET_ENVIRONMENTS, UPDATE_ENVIRONMENT_MUTATION } from "../queries";
import { IEnvironmentsAttr, IHistoricState } from "../types";

interface IEnvironmentsProps {
  projectName: string;
}

const environments: React.FC<IEnvironmentsProps> = (props: IEnvironmentsProps): JSX.Element => {
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  // GraphQL operations
  const { data, refetch } = useQuery(GET_ENVIRONMENTS, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred loading project envs", error);
    },
    variables: { projectName: props.projectName },
  });
  const [addEnvironments] = useMutation(ADD_ENVIRONMENTS_MUTATION, {
    onCompleted: refetch,
    onError: (envsError: ApolloError): void => {
      envsError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Parameter is not valid":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - One or more values already exist":
            msgError(translate.t("search_findings.tab_resources.repeated_item"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding environments", envsError);
        }
      });
    },
  });
  const [updateEnvironment] = useMutation(UPDATE_ENVIRONMENT_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectEnv", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_change"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred updating environment state", error);
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

  const handleEnvAdd: ((values: { resources: IEnvironmentsAttr[] }) => void) = (
    values: { resources: IEnvironmentsAttr[] },
  ): void => {
    const repeatedInputs: IEnvironmentsAttr[] = values.resources.filter((env: IEnvironmentsAttr) =>
      values.resources.filter(_.matches(env)).length > 1);
    const repeatedEnvs: IEnvironmentsAttr[] = values.resources.filter((env: IEnvironmentsAttr) =>
      envsDataset.filter(_.matches(env)).length > 0);

    if (repeatedInputs.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_input"));
    } else if (repeatedEnvs.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      closeAddModal();
      addEnvironments({
        variables: {
          envs: values.resources,
          projectName: props.projectName,
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
        <Can do="backend_api_resolvers_resource__do_add_environments">
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
      <Can do="backend_api_resolvers_resource__do_update_environment" passThrough={true}>
        {(canUpdate: boolean): JSX.Element => (
      <ConfirmDialog title="Change environment state">
        {(confirm: ConfirmFn): React.ReactNode => {
          const handleStateUpdate: ((env: Dictionary<string>) => void) = (env: Dictionary<string>): void => {
            confirm(() => {
              updateEnvironment({
                variables: {
                  env: { urlEnv: env.urlEnv },
                  projectName: props.projectName,
                  state: env.state === "Active" ? "INACTIVE" : "ACTIVE",
                },
              })
                .catch();
            });
          };

          const sortState: ((dataField: string, order: SortOrder) => void) = (
            dataField: string, order: SortOrder,
          ): void => {
            const newSorted: Sorted = { dataField, order };
            sessionStorage.setItem("envSort", JSON.stringify(newSorted));
          };

          const filterState: {} = selectFilter({
            defaultValue: _.get(sessionStorage, "envStateFilter"),
            onFilter: (filterVal: string): void => {
              sessionStorage.setItem("envStateFilter", filterVal);
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
              dataset={envsDataset}
              defaultSorted={JSON.parse(_.get(sessionStorage, "envSort", "{}"))}
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
        )}
      </Can>
      <label>
        <b>{translate.t("search_findings.tab_resources.total_envs")}</b>{envsDataset.length}
      </label>
      <AddEnvironmentsModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleEnvAdd} />
    </React.StrictMode>
  );
};

export { environments as Environments };
