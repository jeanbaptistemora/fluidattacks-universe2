import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faAngleDown,
  faComment,
  faHeadset,
  faQuestionCircle,
  faUpload,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import React, { useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import { UpgradeGroupsModal } from "./UpgradeGroupsModal";

import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { clickedPortal } from "../utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddFilesBasicModal } from "scenes/Dashboard/components/AddFilesBasicModal";
import { SIGN_POST_URL_REQUESTER_MUTATION } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type { IOrganizationGroups } from "scenes/Dashboard/types";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { toggleZendesk } from "utils/widgets";

interface IAddFiles {
  signPostUrlRequester: {
    url: {
      url: string;
      fields: {
        awsaccesskeyid: string;
        key: string;
        policy: string;
        signature: string;
      };
    };
  };
}

interface IHelpWidgetProps {
  groups: IOrganizationGroups["groups"];
}

export const HelpWidget: React.FC<IHelpWidgetProps> = ({
  groups,
}: IHelpWidgetProps): JSX.Element => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setIsDropdownOpen((currentValue): boolean => !currentValue);
  }, []);
  const ref = useDetectClickOutside({
    onTriggered: (event): void => {
      // Exclude clicks in portals to prevent modals from closing the dropdown
      if (!clickedPortal(event)) {
        setIsDropdownOpen(false);
      }
    },
  });

  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);
  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (match) {
      const { groupName } = match.params;
      const currentGroup = groups.find(
        (group): boolean => group.name === groupName
      );
      const serviceAttributes =
        currentGroup === undefined ? [] : currentGroup.serviceAttributes;

      if (
        serviceAttributes.includes("has_squad") &&
        serviceAttributes.includes("is_continuous")
      ) {
        openPopupWidget({
          prefill: {
            customAnswers: { a1: groupName },
            email: userEmail,
            name: userName,
          },
          url: "https://calendly.com/fluidattacks/talk-to-an-expert",
        });
      } else {
        setIsUpgradeOpen(true);
      }
    }
  }, [groups, match, userEmail, userName]);

  const [isButtonEnabled, setIsButtonEnabled] = useState(false);
  const disableButton: () => void = useCallback((): void => {
    setIsButtonEnabled(true);
  }, []);

  const enableButton: () => void = useCallback((): void => {
    setIsButtonEnabled(false);
  }, []);

  const [uploadFile] = useMutation(SIGN_POST_URL_REQUESTER_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred uploading group files", error);
      });
    },
    variables: {
      filesData: userName,
      groupName: userEmail,
    },
  });

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(false);
  }, []);

  async function handleUpload(values: { file: FileList }): Promise<void> {
    disableButton();
    const results = await uploadFile({
      variables: {
        filesData: JSON.stringify([
          {
            fileName: values.file[0].name,
          },
        ]),
        groupName: userEmail,
      },
    });

    const { signPostUrlRequester }: IAddFiles = results.data;
    const { url } = signPostUrlRequester;
    const { awsaccesskeyid, key, policy, signature } = url.fields;

    const formData = new FormData();
    formData.append("acl", "private");
    formData.append("AWSAccessKeyId", awsaccesskeyid);
    formData.append("key", key);
    formData.append("policy", policy);
    formData.append("signature", signature);
    formData.append("file", values.file[0], values.file[0].name);

    const response = await fetch(url.url, {
      body: formData,
      method: "POST",
    });

    if (response.ok) {
      msgSuccess(
        t("searchFindings.tabResources.success"),
        t("searchFindings.tabUsers.titleSuccess")
      );
    } else {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred uploading User files", response.json);
      enableButton();
    }
    enableButton();
    closeAddModal();
  }

  return (
    <div ref={ref}>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faQuestionCircle} />
        &nbsp;
        <FontAwesomeIcon icon={faAngleDown} size={"xs"} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton onClick={toggleZendesk}>
              <FontAwesomeIcon icon={faComment} />
              &nbsp;{t("navbar.help.chat")}
            </DropdownButton>
          </li>
          {match ? (
            <li>
              <DropdownButton onClick={openCalendly}>
                <FontAwesomeIcon icon={faHeadset} />
                &nbsp;{t("navbar.help.expert")}
              </DropdownButton>
              {isUpgradeOpen ? (
                <UpgradeGroupsModal
                  groups={groups}
                  onClose={closeUpgradeModal}
                />
              ) : undefined}
            </li>
          ) : undefined}
          <Can do={"api_mutations_sign_post_url_requester_mutate"}>
            <li>
              <TooltipWrapper
                id={"uploadFile"}
                message={t("navbar.uploadFile.tooltip")}
              >
                <DropdownButton onClick={openAddModal}>
                  <FontAwesomeIcon icon={faUpload} />
                  {t("navbar.uploadFile.text")}
                </DropdownButton>
                <AddFilesBasicModal
                  isOpen={isAddModalOpen}
                  isUploading={isButtonEnabled}
                  onClose={closeAddModal}
                  onSubmit={handleUpload}
                />
              </TooltipWrapper>
            </li>
          </Can>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
