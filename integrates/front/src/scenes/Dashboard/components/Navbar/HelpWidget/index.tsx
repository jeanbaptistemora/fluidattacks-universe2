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

import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { TooltipWrapper } from "components/TooltipWrapper";
import { AddFilesModal } from "scenes/Dashboard/components/AddFilesModal";
import { SIGN_POST_URL_REQUESTER_MUTATION } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { toggleZendesk } from "utils/widgets";

interface IAddFiles {
  signPostUrl: {
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

export const HelpWidget: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { userEmail, userName } = useContext(authContext);

  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setDropdownOpen((currentValue): boolean => !currentValue);
  }, []);
  const ref = useDetectClickOutside({
    onTriggered: (): void => {
      setDropdownOpen(false);
    },
  });

  const openCalendly = useCallback((): void => {
    openPopupWidget({
      url: "https://calendly.com/fluidattacks/talk-to-an-expert",
    });
  }, []);

  const [isButtonEnabled, setButtonEnabled] = useState(false);
  const disableButton: () => void = useCallback((): void => {
    setButtonEnabled(true);
  }, []);

  const enableButton: () => void = useCallback((): void => {
    setButtonEnabled(false);
  }, []);

  const [uploadFile] = useMutation(SIGN_POST_URL_REQUESTER_MUTATION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred uploading group files", error);
      });
    },
    variables: {
      filesData: userEmail,
      groupName: userName,
    },
  });

  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setAddModalOpen(false);
  }, []);

  const handleUpload: (values: {
    description: string;
    file: FileList;
  }) => void = async (values: {
    description: string;
    file: FileList;
  }): Promise<void> => {
    disableButton();
    const results = await uploadFile({
      variables: {
        filesData: JSON.stringify([
          {
            description: values.description,
            fileName: values.file[0].name,
          },
        ]),
        groupName: userName,
      },
    });

    const { signPostUrl }: IAddFiles = results.data;
    const { url } = signPostUrl;
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
  };

  return (
    <div ref={ref}>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faQuestionCircle} />
        &nbsp;
        <FontAwesomeIcon icon={faAngleDown} size={"sm"} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton onClick={toggleZendesk}>
              <FontAwesomeIcon icon={faComment} />
              &nbsp;{t("navbar.help.chat")}
            </DropdownButton>
          </li>
          <li>
            <DropdownButton onClick={openCalendly}>
              <FontAwesomeIcon icon={faHeadset} />
              &nbsp;{t("navbar.help.expert")}
            </DropdownButton>
          </li>
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
                <AddFilesModal
                  isOpen={isAddModalOpen}
                  isUploading={isButtonEnabled}
                  onClose={closeAddModal}
                  onSubmit={handleUpload} // eslint-disable-line react/jsx-no-bind -- Unexpected behaviour with no-bind
                />
              </TooltipWrapper>
            </li>
          </Can>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
