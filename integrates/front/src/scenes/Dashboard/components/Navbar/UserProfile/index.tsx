import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faKey,
  faMobileAlt,
  faSignOutAlt,
  faUserCircle,
  faUserCog,
  faUserLock,
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
import { useTranslation } from "react-i18next";
import { Link, useHistory } from "react-router-dom";

import { APITokenModal } from "./APITokenModal";
import { CredentialsModal } from "./CredentialsModal";
import { MobileModal } from "./MobileModal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import type { IRemoveStakeholderAttr } from "./types";

import { AddUserModal } from "../../AddUserModal";
import { ButtonOpacity } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Dropdown } from "components/Dropdown";
import { MenuDivider, MenuItem } from "components/Menu";
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

  const [isCredentialsModalOpen, setIsCredentialsModalOpen] = useState(false);
  const [isMobileModalOpen, setIsMobileModalOpen] = useState(false);
  const [isTokenModalOpen, setIsTokenModalOpen] = useState(false);
  const openCredentialsModal = useCallback((): void => {
    setIsCredentialsModalOpen(true);
  }, []);
  const closeCredentialsModal = useCallback((): void => {
    setIsCredentialsModalOpen(false);
  }, []);
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
      push("/home");
    },
  });

  return (
    <Dropdown
      align={"left"}
      button={
        <ButtonOpacity>
          <FontAwesomeIcon color={"#2e2e38"} icon={faUserCircle} />
        </ButtonOpacity>
      }
    >
      <MenuItem>
        <button>
          <p className={"b f5 ma0"}>{userName}</p>
          <p className={"f5 ma0"}>{userEmail}</p>
          {_.isUndefined(userIntPhone) ? undefined : (
            <p className={"b f5 ma0"}>
              {t("navbar.mobile")}
              &nbsp;
              {userIntPhone}
            </p>
          )}
          {userRole === undefined ? undefined : (
            <p className={"f5 ma0"}>
              {t("navbar.role")}
              &nbsp;
              {t(`userModal.roles.${_.camelCase(userRole)}`)}
            </p>
          )}
          <p className={"f5 ma0"}>
            {t("navbar.featurePreview")}
            &nbsp;
            <Switch
              checked={featurePreview}
              name={"featurePreview"}
              onChange={toggleFeaturePreview}
            />
          </p>
        </button>
      </MenuItem>
      <MenuDivider />
      <MenuItem>
        <button className={"f5"} onClick={openTokenModal}>
          <FontAwesomeIcon icon={faKey} />
          &nbsp;
          {t("navbar.token")}
        </button>
        {isTokenModalOpen ? (
          <APITokenModal onClose={closeTokenModal} open={true} />
        ) : undefined}
      </MenuItem>
      <MenuItem>
        <Link to={"/user/config"}>
          <p className={"f5 ma0"}>
            <FontAwesomeIcon icon={faUserCog} />
            &nbsp;
            {t("navbar.notification")}
          </p>
        </Link>
      </MenuItem>
      <MenuItem>
        <button className={"f5"} onClick={openCredentialsModal}>
          <FontAwesomeIcon icon={faUserLock} />
          &nbsp;
          {t("navbar.credentials")}
        </button>
        {isCredentialsModalOpen ? (
          <CredentialsModal onClose={closeCredentialsModal} />
        ) : undefined}
      </MenuItem>
      <MenuItem>
        <button className={"f5"} onClick={openMobileModal}>
          <FontAwesomeIcon icon={faMobileAlt} />
          &nbsp;
          {t("navbar.mobile")}
        </button>
        {isMobileModalOpen ? (
          <MobileModal onClose={closeMobileModal} />
        ) : undefined}
      </MenuItem>
      <Can do={"api_mutations_add_stakeholder_mutate"}>
        <MenuItem>
          <button className={"f5 ma0"} onClick={openStakeholderModal}>
            <FontAwesomeIcon icon={faUserPlus} />
            &nbsp;
            {t("navbar.user")}
          </button>
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
        </MenuItem>
      </Can>
      <MenuItem>
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
              <button className={"f5"} onClick={handleLogoutClick}>
                <FontAwesomeIcon icon={faUserTimes} />
                &nbsp;
                {t("navbar.deleteAccount.text")}
              </button>
            );
          }}
        </ConfirmDialog>
      </MenuItem>
      <MenuDivider />
      <MenuItem>
        <ConfirmDialog title={t("navbar.logout")}>
          {(confirm): React.ReactNode => {
            function handleLogoutClick(): void {
              confirm((): void => {
                mixpanel.reset();
                location.assign("/logout");
              });
            }

            return (
              <button className={"f5"} onClick={handleLogoutClick}>
                <FontAwesomeIcon icon={faSignOutAlt} />
                &nbsp;
                {t("navbar.logout")}
              </button>
            );
          }}
        </ConfirmDialog>
      </MenuItem>
    </Dropdown>
  );
};
