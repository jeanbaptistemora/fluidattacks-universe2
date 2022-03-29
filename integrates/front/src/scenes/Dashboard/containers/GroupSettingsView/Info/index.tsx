import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EditGroupInformationModal } from "scenes/Dashboard/components/EditGroupInformationModal";
import { UPDATE_GROUP_INFO } from "scenes/Dashboard/components/EditGroupInformationModal/queries";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { handleEditGroupDataError } from "scenes/Dashboard/containers/GroupSettingsView/Services/helpers";
import type { IGroupData } from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import { ButtonToolbar, Col40, Col60, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const GroupInformation: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isGroupSettingsModalOpen, setGroupSettingsModalOpen] = useState(false);
  const openEditGroupInformationModal: () => void = useCallback((): void => {
    setGroupSettingsModalOpen(true);
  }, []);
  const closeEditGroupInformationModal: () => void = useCallback((): void => {
    setGroupSettingsModalOpen(false);
  }, []);

  const attributeMapper = (attribute: string): string => {
    /**
     * Needed for the new attribute headers of the dataset that do not match
     * the underlying field names
     */
    if (attribute === "Business Registration Number") {
      return "businessId";
    } else if (attribute === "Business Name") {
      return "businessName";
    }

    return attribute.toLocaleLowerCase();
  };

  const formatDataSet = (
    attributes: {
      attribute: string;
      value: string;
    }[]
  ): Record<string, string> => {
    return attributes.reduce(
      (
        acc: Record<string, string>,
        cur: {
          attribute: string;
          value: string;
        }
      ): Record<string, string> => ({
        ...acc,
        [attributeMapper(cur.attribute)]: cur.value,
      }),
      {}
    );
  };

  const { data, refetch: refetchGroupData } = useQuery<IGroupData>(
    GET_GROUP_DATA,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorText"));
          Logger.warning("An error occurred getting group data", error);
        });
      },
      variables: { groupName },
    }
  );

  const [editGroupInfo] = useMutation(UPDATE_GROUP_INFO, {
    onCompleted: async (): Promise<void> => {
      mixpanel.track("EditGroupData");
      msgSuccess(
        t("groupAlerts.groupInfoUpdated"),
        t("groupAlerts.titleSuccess")
      );
      await refetchGroupData({ groupName });
    },
    onError: (error: ApolloError): void => {
      handleEditGroupDataError(error);
    },
  });

  const handleFormSubmit = useCallback(
    async (values: Record<string, string>): Promise<void> => {
      await editGroupInfo({
        variables: {
          businessId: values.businessId,
          businessName: values.businessName,
          description: values.description,
          groupName,
          language: values.language,
        },
      });
      setGroupSettingsModalOpen(false);
    },
    [editGroupInfo, groupName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }
  const attributesDataset: {
    attribute: string;
    value: string;
  }[] = [
    {
      attribute: "Language",
      value: data.group.language,
    },
    {
      attribute: "Description",
      value: data.group.description,
    },
    {
      attribute: "Business Registration Number",
      value: data.group.businessId,
    },
    {
      attribute: "Business Name",
      value: data.group.businessName,
    },
  ];
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "attribute",
      header: "Attribute",
    },
    {
      dataField: "value",
      formatter: (value: string): string => {
        const mappedLanguage = {
          EN: "English",
          ES: "Spanish",
        }[value];

        if (!_.isUndefined(mappedLanguage)) {
          return mappedLanguage;
        }

        return value;
      },
      header: "Value",
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col60 className={"pa0"}>
          <h2>{t("searchFindings.infoTable.title")}</h2>
        </Col60>
        <Col40>
          <ButtonToolbar>
            <Can do={"api_mutations_update_group_stakeholder_mutate"}>
              <TooltipWrapper
                displayClass={"dib"}
                id={"searchFindings.tabUsers.editButton.tooltip.id"}
                message={t(
                  "searchFindings.tabResources.information.btnTooltip"
                )}
              >
                <Button
                  disabled={permissions.cannot(
                    "api_mutations_update_group_mutate"
                  )}
                  id={"editGroup"}
                  onClick={openEditGroupInformationModal}
                  variant={"secondary"}
                >
                  <FluidIcon icon={"edit"} />
                  &nbsp;
                  {t("searchFindings.tabUsers.editButton.text")}
                </Button>
              </TooltipWrapper>
            </Can>
          </ButtonToolbar>
        </Col40>
      </Row>
      <Table
        dataset={attributesDataset}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblGroupInfo"}
        pageSize={10}
        search={false}
      />
      <EditGroupInformationModal
        initialValues={formatDataSet(attributesDataset)}
        isOpen={isGroupSettingsModalOpen}
        onClose={closeEditGroupInformationModal}
        onSubmit={handleFormSubmit}
      />
    </React.StrictMode>
  );
};

export { GroupInformation };
