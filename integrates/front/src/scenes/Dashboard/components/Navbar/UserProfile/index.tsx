import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faKey,
  faMobileAlt,
  faSignOutAlt,
  faUserCircle,
  faUserCog,
  faUserPlus,
  faUserTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { useDetectClickOutside } from "react-detect-click-outside";
import { useTranslation } from "react-i18next";
import { Link, useHistory } from "react-router-dom";

import { APITokenModal } from "./APITokenModal";
import { MobileModal } from "./MobileModal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import type { IRemoveStakeholderAttr } from "./types";

import { AddUserModal } from "../../AddUserModal";
import { DropdownButton, DropdownDivider, DropdownMenu } from "../styles";
import { clickedPortal } from "../utils";
import { ButtonOpacity } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Switch } from "components/Switch";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import { Alert, ControlLabel } from "styles/styledComponents";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import type { IFeaturePreviewContext } from "utils/featurePreview";
import { featurePreviewContext } from "utils/featurePreview";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IUserProfileProps {
  userRole: string | undefined;
}

export const UserProfile: React.FC<IUserProfileProps> = ({
  userRole,
}: IUserProfileProps): JSX.Element => {
  const { userEmail, userName, userIntPhone } = useContext(authContext);
  const { t } = useTranslation();
  const { push } = useHistory();

  const { featurePreview, setFeaturePreview } = useContext(
    featurePreviewContext as React.Context<Required<IFeaturePreviewContext>>
  );
  const toggleFeaturePreview = useCallback((): void => {
    setFeaturePreview((currentValue): boolean => {
      mixpanel.track(`${currentValue ? "Disable" : "Enable"}FeaturePreview`);

      return !currentValue;
    });
  }, [setFeaturePreview]);

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

  const [isMobileModalOpen, setIsMobileModalOpen] = useState(false);
  const [isTokenModalOpen, setIsTokenModalOpen] = useState(false);
  const openMobileModal = useCallback((): void => {
    setIsMobileModalOpen(true);
  }, []);
  const closeMobileModal = useCallback((): void => {
    setIsMobileModalOpen(false);
  }, []);
  const openTokenModal = useCallback((): void => {
    setIsTokenModalOpen(true);
  }, []);
  const closeTokenModal = useCallback((): void => {
    setIsTokenModalOpen(false);
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
        msgSuccess(
          t("navbar.deleteAccount.success"),
          t("navbar.deleteAccount.successTitle")
        );
        toggleDropdown();
      } else {
        push("/home");
      }
    },
    onError: (removeError: ApolloError): void => {
      removeError.graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - The previous invitation to this user was requested less than a minute ago"
        ) {
          msgError(t("navbar.deleteAccount.requestedTooSoon"));
        } else {
          Logger.error("An error occurred while deleting account", error);
          msgError(t("groupAlerts.errorTextsad"));
        }
      });
      toggleDropdown();
      push("/home");
    },
  });

  return (
    <div ref={ref}>
      <ButtonOpacity onClick={toggleDropdown}>
        <FontAwesomeIcon color={"#2e2e38"} icon={faUserCircle} />
      </ButtonOpacity>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <DropdownButton>
              <b>{userName}</b>
              <br />
              {userEmail}
              {_.isUndefined(userIntPhone) ? undefined : (
                <React.Fragment>
                  <br />
                  {t("navbar.mobile")}
                  {":"}&nbsp;
                  {userIntPhone}
                </React.Fragment>
              )}
              {userRole === undefined ? undefined : (
                <React.Fragment>
                  <br />
                  {t("navbar.role")}&nbsp;
                  {t(`userModal.roles.${_.camelCase(userRole)}`)}
                </React.Fragment>
              )}
              <br />
              {t("navbar.featurePreview")}&nbsp;
              <Switch
                checked={featurePreview}
                name={"featurePreview"}
                onChange={toggleFeaturePreview}
              />
            </DropdownButton>
          </li>
          <DropdownDivider />
          <li>
            <DropdownButton onClick={openTokenModal}>
              <FontAwesomeIcon icon={faKey} />
              &nbsp;
              {t("navbar.token")}
            </DropdownButton>
            {isTokenModalOpen ? (
              <APITokenModal onClose={closeTokenModal} open={true} />
            ) : undefined}
          </li>
          <li>
            <Link onClick={toggleDropdown} to={"/user/config"}>
              <DropdownButton>
                <FontAwesomeIcon icon={faUserCog} />
                &nbsp;
                {t("navbar.notification")}
              </DropdownButton>
            </Link>
          </li>
          <li>
            <DropdownButton onClick={openMobileModal}>
              <FontAwesomeIcon icon={faMobileAlt} />
              &nbsp;
              {t("navbar.mobile")}
            </DropdownButton>
            {isMobileModalOpen ? (
              <MobileModal onClose={closeMobileModal} />
            ) : undefined}
          </li>
          <Can do={"api_mutations_add_stakeholder_mutate"}>
            <li>
              <DropdownButton onClick={openStakeholderModal}>
                <FontAwesomeIcon icon={faUserPlus} />
                &nbsp;
                {t("navbar.user")}
              </DropdownButton>
              {isStakeholderModalOpen ? (
                <AddUserModal
                  action={"add"}
                  editTitle={""}
                  initialValues={{}}
                  onClose={closeStakeholderModal}
                  onSubmit={handleAddUserSubmit}
                  open={true}
                  title={t("navbar.user")}
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
                  <DropdownButton onClick={handleLogoutClick}>
                    <FontAwesomeIcon icon={faUserTimes} />
                    &nbsp;
                    {t("navbar.deleteAccount.text")}
                  </DropdownButton>
                );
              }}
            </ConfirmDialog>
          </li>
          <DropdownDivider />
          <li>
            <ConfirmDialog title={t("navbar.logout")}>
              {(confirm): React.ReactNode => {
                function handleLogoutClick(): void {
                  confirm((): void => {
                    mixpanel.reset();
                    location.assign("/logout");
                  });
                }

                return (
                  <DropdownButton onClick={handleLogoutClick}>
                    <FontAwesomeIcon icon={faSignOutAlt} />
                    &nbsp;
                    {t("navbar.logout")}
                  </DropdownButton>
                );
              }}
            </ConfirmDialog>
          </li>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
