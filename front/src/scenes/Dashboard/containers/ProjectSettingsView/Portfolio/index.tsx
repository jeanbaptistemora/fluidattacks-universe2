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
import { Button } from "../../../../../components/Button";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { AddTagsModal } from "../../../components/AddTagsModal/index";
import { ADD_TAGS_MUTATION, GET_TAGS, REMOVE_TAG_MUTATION } from "../queries";

interface IPortfolioProps {
  groupRole: string;
  projectName: string;
}

const portfolio: React.FC<IPortfolioProps> = (props: IPortfolioProps): JSX.Element => {
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // State management
  const [isAddModalOpen, setAddModalOpen] = React.useState(false);
  const openAddModal: (() => void) = (): void => { setAddModalOpen(true); };
  const closeAddModal: (() => void) = (): void => { setAddModalOpen(false); };

  const [currentRow, setCurrentRow] = React.useState<Dictionary<string>>({});

  // GraphQL operations
  const { data, refetch, networkStatus } = useQuery(GET_TAGS, {
    notifyOnNetworkStatusChange: true,
    variables: { projectName: props.projectName },
  });

  const [addTags] = useMutation(ADD_TAGS_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("AddProjectTags", { Organization: userOrganization, User: userName });
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
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred adding tags", error);
        }
      });
    },
  });

  const [removeTag, { loading: removing }] = useMutation(REMOVE_TAG_MUTATION, {
    onCompleted: (): void => {
      refetch()
        .catch();
      mixpanel.track("RemoveProjectEnv", { Organization: userOrganization, User: userName });
      msgSuccess(
        translate.t("search_findings.tab_resources.success_remove"),
        translate.t("search_findings.tab_users.title_success"),
      );
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred removing tags", error);
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
      addTags({
        variables: {
          projectName: props.projectName,
          tagsData: JSON.stringify(values.tags),
        },
      })
        .catch();
    }
  };

  const handleRemoveTag: (() => void) = (): void => {
    removeTag({
      variables: {
        projectName: props.projectName,
        tagToRemove: currentRow.tagName,
      },
    })
      .catch();
    setCurrentRow({});
  };

  const sortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("portfolioSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeader[] = [
    {
      dataField: "tagName",
      header: translate.t("search_findings.tab_resources.tags_title"),
      onSort: sortState,
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.tab_resources.tags_title")}</h3>
        </Col>
        {_.includes(["admin", "customer", "customeradmin"], props.groupRole) ? (
          <Col lg={4} md={2} xs={5}>
            <ButtonToolbar className="pull-right">
              <Button onClick={openAddModal}>
                <Glyphicon glyph="plus" />&nbsp;
              {translate.t("search_findings.tab_resources.add_repository")}
              </Button>
              <Button onClick={handleRemoveTag} disabled={_.isEmpty(currentRow) || removing}>
                <Glyphicon glyph="minus" />&nbsp;
              {translate.t("search_findings.tab_resources.remove_repository")}
              </Button>
            </ButtonToolbar>
          </Col>
        ) : undefined}
      </Row>
      <DataTableNext
        bordered={true}
        dataset={tagsDataset}
        defaultSorted={JSON.parse(_.get(sessionStorage, "portfolioSort", "{}"))}
        exportCsv={false}
        search={false}
        headers={tableHeaders}
        id="tblTags"
        pageSize={15}
        remote={false}
        striped={true}
        selectionMode={{
          clickToSelect: _.includes(["admin", "customer", "customeradmin"], props.groupRole),
          hideSelectColumn: !_.includes(["admin", "customer", "customeradmin"], props.groupRole),
          mode: "radio",
          onSelect: networkStatus === NetworkStatus.refetch || removing ? undefined : setCurrentRow,
        }}
      />
      <AddTagsModal isOpen={isAddModalOpen} onClose={closeAddModal} onSubmit={handleTagsAdd} />
    </React.StrictMode>
  );
};

export { portfolio as Portfolio };
