/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError, NetworkStatus } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";

import { Badge } from "components/Badge";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { IHeaderConfig } from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddTagsModal } from "scenes/Dashboard/components/AddTagsModal";
import { ADD_TAGS_MUTATION, GET_TAGS,
  REMOVE_TAG_MUTATION,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

export interface IPortfolioProps {
  projectName: string;
}

const portfolio: React.FC<IPortfolioProps> = (props: IPortfolioProps): JSX.Element => {
  const { userName } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});

  // GraphQL operations
  const { data, refetch, networkStatus } = useQuery(GET_TAGS, {
    notifyOnNetworkStatusChange: true,
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading project tags", error);
    },
    variables: { projectName: props.projectName },
  });

  const [addTags] = useMutation(ADD_TAGS_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("AddProjectTags", { User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - One or more values already exist":
            msgError(translate.t("search_findings.tab_resources.repeated_item"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred adding tags", error);
        }
      });
    },
  });

  const [removeTag, { loading: removing }] = useMutation(REMOVE_TAG_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("RemoveProjectEnv", { User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_remove"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred removing tags", error);
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const tagsDataset: Array<{ tagName: string }> = data.project.tags.map((tag: string) => ({ tagName: tag }));

  const handleTagsAdd: ((values: { tags: string[] }) => void) = (values: { tags: string[] }): void => {
    const repeatedInputs: string[] = values.tags.filter((tag: string) =>
      values.tags.filter(_.matches(tag)).length > 1);
    const repeatedTags: string[] = values.tags.filter((tag: string) =>
      tagsDataset.filter(_.matches({ tagName: tag })).length > 0);

    if (repeatedInputs.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_input"));
    } else if (repeatedTags.length > 0) {
      msgError(translate.t("search_findings.tab_resources.repeated_item"));
    } else {
      closeAddModal();
      void addTags({
        variables: {
          projectName: props.projectName,
          tagsData: JSON.stringify(values.tags),
        },
      });
    }
  };

  const handleRemoveTag: (() => void) = (): void => {
    void removeTag({
      variables: {
        projectName: props.projectName,
        tagToRemove: currentRow.tagName,
      },
    });
    setCurrentRow({});
  };

  const sortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("portfolioSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "tagName",
      header: translate.t("search_findings.tab_resources.tags.title"),
      onSort: sortState,
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.tab_resources.tags.title")}<Badge>pro</Badge></h3>
        </Col>
        <Col lg={4} md={2} xs={5}>
          <ButtonToolbar className="pull-right">
            <Can do="backend_api_resolvers_project__do_add_tags">
              <TooltipWrapper
                message={translate.t("search_findings.tab_resources.tags.add_tooltip")}
                placement="top"
              >
                <Button onClick={openAddModal}>
                  <Glyphicon glyph="plus" />&nbsp;
                {translate.t("search_findings.tab_resources.add_repository")}
                </Button>
              </TooltipWrapper>
            </Can>
            <Can do="backend_api_resolvers_project__do_remove_tag">
              <TooltipWrapper
                message={translate.t("search_findings.tab_resources.tags.remove_tooltip")}
                placement="top"
              >
                <Button onClick={handleRemoveTag} disabled={_.isEmpty(currentRow) || removing}>
                  <Glyphicon glyph="minus" />&nbsp;
                {translate.t("search_findings.tab_resources.remove_repository")}
                </Button>
              </TooltipWrapper>
            </Can>
          </ButtonToolbar>
        </Col>
      </Row>
      <Can do="backend_api_resolvers_project__do_remove_tag" passThrough={true}>
        {(canDelete: boolean): JSX.Element => (
          <DataTableNext
            bordered={true}
            dataset={tagsDataset}
            defaultSorted={JSON.parse(_.get(sessionStorage, "portfolioSort", "{}"))}
            exportCsv={false}
            search={false}
            headers={tableHeaders}
            id="tblTags"
            pageSize={15}
            striped={true}
            selectionMode={{
              clickToSelect: canDelete,
              hideSelectColumn: !canDelete,
              mode: "radio",
              onSelect: networkStatus === NetworkStatus.refetch || removing ? undefined : setCurrentRow,
            }}
          />
        )}
      </Can>
      <AddTagsModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleTagsAdd} />
    </React.StrictMode>
  );
};

export { portfolio as Portfolio };
