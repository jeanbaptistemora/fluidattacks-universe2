import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
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
import { translate } from "utils/translations/translate";

const GroupInformation: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isGroupSettingsModalOpen, setGroupSettingsModalOpen] = useState(false);
  const openEditGroupInformationModal: () => void = useCallback((): void => {
    setGroupSettingsModalOpen(true);
  }, []);
  const closeEditGroupInformationModal: () => void = useCallback((): void => {
    setGroupSettingsModalOpen(false);
  }, []);

  const formatDataSet: (
    attributes: {
      attribute: string;
      value: string;
    }[]
  ) => Record<string, string> = (
    attributes: {
      attribute: string;
      value: string;
    }[]
  ): Record<string, string> => {
    return attributes.reduce(
      // Type specification not necessary
      // eslint-disable-next-line @typescript-eslint/explicit-function-return-type
      (acc, cur) => ({
        ...acc,
        [cur.attribute.toLocaleLowerCase()]: cur.value,
      }),
      {}
    );
  };

  const { data, refetch: refetchGroupData } = useQuery<IGroupData>(
    GET_GROUP_DATA,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorText"));
          Logger.warning("An error occurred getting group data", error);
        });
      },
      variables: { groupName },
    }
  );

  const [editGroupInfo] = useMutation(UPDATE_GROUP_INFO, {
    onCompleted: (): void => {
      track("EditGroupData");
      msgSuccess(
        translate.t("groupAlerts.groupInfoUpdated"),
        translate.t("groupAlerts.titleSuccess")
      );
      void refetchGroupData({ groupName });
    },
    onError: (error: ApolloError): void => {
      handleEditGroupDataError(error);
    },
  });

  const handleFormSubmit = useCallback(
    (values: Record<string, string>): void => {
      void editGroupInfo({
        variables: {
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
      // Next annotations needed as DB queries use "any" type
      // eslint-disable-next-line @typescript-eslint/restrict-template-expressions, @typescript-eslint/no-unsafe-member-access
      value: data.group.language,
    },
    {
      attribute: "Description",
      // Next annotations needed as DB queries use "any" type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      value: data.group.description,
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
          <h2>{translate.t("searchFindings.infoTable.title")}</h2>
        </Col60>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <Col40>
          <ButtonToolbar>
            <Can do={"api_mutations_update_group_stakeholder_mutate"}>
              <TooltipWrapper
                displayClass={"dib"}
                id={"searchFindings.tabUsers.editButton.tooltip.id"}
                message={translate.t(
                  "searchFindings.tabResources.information.btnTooltip"
                )}
              >
                <Button
                  disabled={permissions.cannot(
                    "api_mutations_update_group_mutate"
                  )}
                  id={"editGroup"}
                  onClick={openEditGroupInformationModal}
                >
                  <FluidIcon icon={"edit"} />
                  &nbsp;
                  {translate.t("searchFindings.tabUsers.editButton.text")}
                </Button>
              </TooltipWrapper>
            </Can>
          </ButtonToolbar>
        </Col40>
      </Row>
      <DataTableNext
        bordered={true}
        dataset={attributesDataset}
        exportCsv={false}
        headers={tableHeaders}
        id={"tblGroupInfo"}
        pageSize={10}
        search={false}
        striped={true}
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
