import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faAngleDown,
  faKey,
  faSignOutAlt,
  faUserCircle,
  faUserCog,
  faUserPlus,
  faUserSlash,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { reset, track } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { APITokenModal } from "./APITokenModal";
import { GlobalConfigModal } from "./GlobalConfigModal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import type { IRemoveStakeholderAttr } from "./types";

import { AddUserModal } from "../../AddUserModal";
import {
  DropdownButton,
  DropdownDivider,
  DropdownMenu,
  NavbarButton,
} from "../styles";
import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import { Alert, ControlLabel } from "styles/styledComponents";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IUserProfileProps {
  userRole: string | undefined;
}

export const UserProfile: React.FC<IUserProfileProps> = ({
  userRole,
}: IUserProfileProps): JSX.Element => {
  const { userEmail, userName } = useContext(authContext);
  const { t } = useTranslation();
  const { push } = useHistory();

  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setDropdownOpen((currentValue): boolean => !currentValue);
  }, []);
  const ref = useDetectClickOutside({
    onTriggered: (): void => {
      setDropdownOpen(false);
    },
  });

  const [isTokenModalOpen, setTokenModalOpen] = useState(false);
  const openTokenModal = useCallback((): void => {
    setTokenModalOpen(true);
  }, []);
  const closeTokenModal = useCallback((): void => {
    setTokenModalOpen(false);
  }, []);

  const [isConfigModalOpen, setConfigModalOpen] = useState(false);
  const openConfigModal: () => void = useCallback((): void => {
    setConfigModalOpen(true);
    track("OpenGlobalConfig");
  }, []);
  const closeConfigModal: () => void = useCallback((): void => {
    setConfigModalOpen(false);
  }, []);

  const [addStakeholder, isStakeholderModalOpen, setStakeholderModalOpen] =
    useAddStakeholder();
  const handleAddUserSubmit = useCallback(
    (values): void => {
      void addStakeholder({ variables: values });
    },
    [addStakeholder]
  );
  const openStakeholderModal = useCallback((): void => {
    setStakeholderModalOpen(true);
  }, [setStakeholderModalOpen]);
  const closeStakeholderModal = useCallback((): void => {
    setStakeholderModalOpen(false);
  }, [setStakeholderModalOpen]);

  const [removeStakeholder] = useMutation(REMOVE_STAKEHOLDER_MUTATION, {
    onCompleted: (mtResult: IRemoveStakeholderAttr): void => {
      if (mtResult.removeStakeholder.success) {
        reset();
        location.assign("/logout");
      } else {
        push("/home");
      }
    },
    onError: (removeError: ApolloError): void => {
      removeError.graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("An error occurred while deleting account", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
      push("/home");
    },
  });

  return (
    <div ref={ref}>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faUserCircle} />
        &nbsp;
        <FontAwesomeIcon icon={faAngleDown} size={"sm"} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton>
              <b>{userName}</b>
              <br />
              {userEmail}
              {userRole === undefined ? undefined : (
                <React.Fragment>
                  <br />
                  {t("navbar.role")}&nbsp;
                  {t(`userModal.roles.${_.camelCase(userRole)}`)}
                </React.Fragment>
              )}
            </DropdownButton>
          </li>
          <DropdownDivider />
          <li>
            <DropdownButton onClick={openTokenModal}>
              <TooltipWrapper
                id={"apiToken"}
                message={t("navbar.token.tooltip")}
              >
                <FontAwesomeIcon icon={faKey} />
                &nbsp;
                {t("navbar.token.text")}
              </TooltipWrapper>
            </DropdownButton>
            {isTokenModalOpen ? (
              <APITokenModal onClose={closeTokenModal} open={true} />
            ) : undefined}
          </li>
          <li>
            <TooltipWrapper
              id={"globalConfig"}
              message={t("navbar.config.tooltip")}
            >
              <DropdownButton onClick={openConfigModal}>
                <FontAwesomeIcon icon={faUserCog} />
                &nbsp;{t("navbar.config.text")}
              </DropdownButton>
            </TooltipWrapper>
            {isConfigModalOpen ? (
              <GlobalConfigModal onClose={closeConfigModal} open={true} />
            ) : undefined}
          </li>
          <Can do={"api_mutations_add_stakeholder_mutate"}>
            <li>
              <TooltipWrapper id={"addUser"} message={t("navbar.user.tooltip")}>
                <DropdownButton onClick={openStakeholderModal}>
                  <FontAwesomeIcon icon={faUserPlus} />
                  {t("navbar.user.text")}
                </DropdownButton>
              </TooltipWrapper>
              {isStakeholderModalOpen ? (
                <AddUserModal
                  action={"add"}
                  editTitle={""}
                  initialValues={{}}
                  onClose={closeStakeholderModal}
                  onSubmit={handleAddUserSubmit}
                  open={true}
                  title={t("navbar.user.text")}
                  type={"user"}
                />
              ) : undefined}
            </li>
          </Can>
          <li>
            <ConfirmDialog
              message={
                <React.Fragment>
                  <ControlLabel>
                    {t("navbar.deleteAccount.modal.warning")}
                  </ControlLabel>
                  <Alert>{t("navbar.deleteAccount.modal.text")}</Alert>
                </React.Fragment>
              }
              title={t("navbar.deleteAccount.text")}
            >
              {(confirm): React.ReactNode => {
                function handleLogoutClick(): void {
                  confirm((): void => {
                    void removeStakeholder();
                  });
                }

                return (
                  <TooltipWrapper
                    id={"deleteAccount"}
                    message={t("navbar.deleteAccount.tooltip")}
                  >
                    <DropdownButton onClick={handleLogoutClick}>
                      <FontAwesomeIcon icon={faUserSlash} />
                      &nbsp;
                      {t("navbar.deleteAccount.text")}
                    </DropdownButton>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </li>
          <DropdownDivider />
          <li>
            <ConfirmDialog title={t("navbar.logout.text")}>
              {(confirm): React.ReactNode => {
                function handleLogoutClick(): void {
                  confirm((): void => {
                    reset();
                    location.assign("/logout");
                  });
                }

                return (
                  <TooltipWrapper
                    id={"logOut"}
                    message={t("navbar.logout.tooltip")}
                  >
                    <DropdownButton onClick={handleLogoutClick}>
                      <FontAwesomeIcon icon={faSignOutAlt} />
                      &nbsp;
                      {t("navbar.logout.text")}
                    </DropdownButton>
                  </TooltipWrapper>
                );
              }}
            </ConfirmDialog>
          </li>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
