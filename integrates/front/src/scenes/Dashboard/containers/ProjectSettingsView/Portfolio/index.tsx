import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";

import { Badge } from "components/Badge";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddTagsModal } from "scenes/Dashboard/components/AddTagsModal";
import {
  ADD_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_TAG_MUTATION,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import { ButtonToolbar, Col40, Col60, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IPortfolioProps {
  projectName: string;
}

const Portfolio: React.FC<IPortfolioProps> = (
  props: IPortfolioProps
): JSX.Element => {
  const { projectName } = props;

  // State management
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setAddModalOpen(false);
  }, []);

  const [currentRow, setCurrentRow] = useState<Dictionary<string>>({});

  // GraphQL operations
  const { data, refetch, networkStatus } = useQuery(GET_TAGS, {
    notifyOnNetworkStatusChange: true,
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading project tags", error);
    },
    variables: { projectName },
  });

  const [addTags] = useMutation(ADD_TAGS_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      track("AddProjectTags");
      msgSuccess(
        translate.t("searchFindings.tabResources.success"),
        translate.t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - One or more values already exist":
            msgError(translate.t("searchFindings.tabResources.repeatedItem"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred adding tags", error);
        }
      });
    },
  });

  const [removeTag, { loading: removing }] = useMutation(REMOVE_TAG_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      track("RemoveTag");
      msgSuccess(
        translate.t("searchFindings.tabResources.successRemove"),
        translate.t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing tags", error);
      });
    },
  });

  const handleRemoveTag: () => void = useCallback((): void => {
    void removeTag({
      variables: {
        projectName: props.projectName,
        tagToRemove: currentRow.tagName,
      },
    });
    setCurrentRow({});
    // eslint-disable-next-line react/destructuring-assignment -- In conflict with previous declaration
  }, [currentRow.tagName, props.projectName, removeTag]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const tagsDataset: {
    tagName: string;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call -- DB queries use "any" type
  }[] = data.project.tags.map((tag: string): { tagName: string } => ({
    tagName: tag,
  }));

  const handleTagsAdd: (values: { tags: string[] }) => void = (values: {
    tags: string[];
  }): void => {
    const repeatedInputs: string[] = values.tags.filter(
      (tag: string): boolean => values.tags.filter(_.matches(tag)).length > 1
    );
    const repeatedTags: string[] = values.tags.filter(
      (tag: string): boolean =>
        tagsDataset.filter(_.matches({ tagName: tag })).length > 0
    );

    if (repeatedInputs.length > 0) {
      msgError(translate.t("searchFindings.tabResources.repeatedInput"));
    } else if (repeatedTags.length > 0) {
      msgError(translate.t("searchFindings.tabResources.repeatedItem"));
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

  const sortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("portfolioSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "tagName",
      header: translate.t("searchFindings.tabResources.tags.title"),
      onSort: sortState,
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col60 className={"pa0"}>
          <h2>
            {translate.t("searchFindings.tabResources.tags.title")}
            <Badge>{"pro"}</Badge>
          </h2>
        </Col60>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col40 className={"pa0"}>
          <ButtonToolbar>
            <Can do={"backend_api_mutations_add_group_tags_mutate"}>
              <TooltipWrapper
                displayClass={"dib"}
                id={"searchFindings.tabResources.tags.addTooltip.id"}
                message={translate.t(
                  "searchFindings.tabResources.tags.addTooltip"
                )}
                placement={"top"}
              >
                <Button id={"portfolio-add"} onClick={openAddModal}>
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;
                  {translate.t("searchFindings.tabResources.addRepository")}
                </Button>
              </TooltipWrapper>
            </Can>
            <Can do={"backend_api_mutations_remove_group_tag_mutate"}>
              <TooltipWrapper
                displayClass={"dib"}
                id={"searchFindings.tabResources.tags.removeTooltip.id"}
                message={translate.t(
                  "searchFindings.tabResources.tags.removeTooltip"
                )}
                placement={"top"}
              >
                <Button
                  disabled={_.isEmpty(currentRow) || removing}
                  id={"portfolio-remove"}
                  onClick={handleRemoveTag}
                >
                  <FontAwesomeIcon icon={faMinus} />
                  &nbsp;
                  {translate.t("searchFindings.tabResources.removeRepository")}
                </Button>
              </TooltipWrapper>
            </Can>
          </ButtonToolbar>
        </Col40>
      </Row>
      <Can
        do={"backend_api_mutations_remove_group_tag_mutate"}
        passThrough={true}
      >
        {(canDelete: boolean): JSX.Element => (
          <DataTableNext
            bordered={true}
            dataset={tagsDataset}
            defaultSorted={JSON.parse(
              _.get(sessionStorage, "portfolioSort", "{}")
            )}
            exportCsv={false}
            headers={tableHeaders}
            id={"tblTags"}
            pageSize={15}
            search={false}
            selectionMode={{
              clickToSelect: canDelete,
              hideSelectColumn: !canDelete,
              mode: "radio",
              onSelect:
                networkStatus === NetworkStatus.refetch || removing
                  ? undefined
                  : setCurrentRow,
            }}
            striped={true}
          />
        )}
      </Can>
      <AddTagsModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onSubmit={handleTagsAdd} // eslint-disable-line react/jsx-no-bind -- Unexpected behaviour with no-bind
      />
    </React.StrictMode>
  );
};

export { Portfolio, IPortfolioProps };
