import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Gap } from "components/Layout";
import { Table } from "components/Table";
import { Tooltip } from "components/Tooltip";
import { AddTagsModal } from "scenes/Dashboard/components/AddTagsModal";
import {
  ADD_GROUP_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_GROUP_TAG_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import type { IGetTagsQuery } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/types";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IPortfolioProps {
  groupName: string;
}

const Portfolio: React.FC<IPortfolioProps> = ({
  groupName,
}: IPortfolioProps): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(false);
  }, []);

  const [currentRow, setCurrentRow] = useState<{ tagName: string }[]>([]);

  // GraphQL operations
  const { data, refetch, networkStatus } = useQuery<IGetTagsQuery>(GET_TAGS, {
    onError: (error: ApolloError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group tags", error);
    },
    variables: { groupName },
  });

  const [addGroupTags] = useMutation(ADD_GROUP_TAGS_MUTATION, {
    onCompleted: (): void => {
      void refetch();
      mixpanel.track("AddGroupTags");
      msgSuccess(
        t("searchFindings.tabResources.success"),
        t("searchFindings.tabUsers.titleSuccess")
      );
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        if (message === "Exception - One or more values already exist") {
          msgError(t("searchFindings.tabResources.repeatedItem"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred adding tags", error);
        }
      });
    },
  });

  const [removeGroupTag, { loading: removing }] = useMutation(
    REMOVE_GROUP_TAG_MUTATION,
    {
      onCompleted: (): void => {
        void refetch();
        mixpanel.track("RemoveTag");
        msgSuccess(
          t("searchFindings.tabResources.successRemove"),
          t("searchFindings.tabUsers.titleSuccess")
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred removing tags", error);
        });
      },
    }
  );

  const handleRemoveTag = useCallback(async (): Promise<void> => {
    await removeGroupTag({
      variables: {
        groupName,
        tagToRemove: currentRow[0].tagName,
      },
    });
    setCurrentRow([]);
  }, [currentRow, groupName, removeGroupTag]);

  const groupTags =
    _.isUndefined(data) || _.isNull(data.group.tags) ? [] : data.group.tags;

  const tagsDataset: {
    tagName: string;
  }[] = groupTags.map((tag: string): { tagName: string } => ({
    tagName: tag,
  }));

  const handleTagsAdd = useCallback(
    async (values: { tags: string[] }): Promise<void> => {
      const repeatedInputs: string[] = values.tags.filter(
        (tag: string): boolean => values.tags.filter(_.matches(tag)).length > 1
      );
      const repeatedTags: string[] = values.tags.filter(
        (tag: string): boolean =>
          tagsDataset.filter(_.matches({ tagName: tag })).length > 0
      );

      if (repeatedInputs.length > 0) {
        msgError(t("searchFindings.tabResources.repeatedInput"));
      } else if (repeatedTags.length > 0) {
        msgError(t("searchFindings.tabResources.repeatedItem"));
      } else {
        closeAddModal();
        await addGroupTags({
          variables: {
            groupName,
            tagsData: JSON.stringify(values.tags),
          },
        });
      }
    },
    [addGroupTags, closeAddModal, groupName, t, tagsDataset]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const columns: ColumnDef<{ tagName: string }>[] = [
    {
      accessorKey: "tagName",
      header: t("searchFindings.tabResources.tags.title"),
    },
  ];

  return (
    <React.StrictMode>
      <Gap>
        <Can do={"api_mutations_add_group_tags_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabResources.tags.addTooltip.id"}
            place={"top"}
            tip={t("searchFindings.tabResources.tags.addTooltip")}
          >
            <Button
              id={"portfolio-add"}
              onClick={openAddModal}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faPlus} />
              &nbsp;
              {t("searchFindings.tabResources.addRepository")}
            </Button>
          </Tooltip>
        </Can>
        <Can do={"api_mutations_remove_group_tag_mutate"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabResources.tags.removeTooltip.id"}
            place={"top"}
            tip={t("searchFindings.tabResources.tags.removeTooltip")}
          >
            <Button
              disabled={_.isEmpty(currentRow) || removing}
              id={"portfolio-remove"}
              onClick={handleRemoveTag}
              variant={"secondary"}
            >
              <FontAwesomeIcon icon={faMinus} />
              &nbsp;
              {t("searchFindings.tabResources.removeRepository")}
            </Button>
          </Tooltip>
        </Can>
      </Gap>
      <Can do={"api_mutations_remove_group_tag_mutate"} passThrough={true}>
        {(canDelete: boolean): JSX.Element => (
          <Table
            columns={columns}
            data={tagsDataset}
            id={"tblTags"}
            rowSelectionSetter={
              canDelete &&
              !(networkStatus === NetworkStatus.refetch || removing)
                ? setCurrentRow
                : undefined
            }
            rowSelectionState={currentRow}
            selectionMode={"radio"}
          />
        )}
      </Can>
      <AddTagsModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onSubmit={handleTagsAdd}
      />
    </React.StrictMode>
  );
};

export type { IPortfolioProps };
export { Portfolio };
