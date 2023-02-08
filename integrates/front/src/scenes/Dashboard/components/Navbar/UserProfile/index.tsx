import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faKey,
  faMobileAlt,
  faSignOutAlt,
  faUser,
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
import { useTranslation } from "react-i18next";
import { Link, useHistory } from "react-router-dom";

import { APITokenModal } from "./APITokenModal";
import { MobileModal } from "./MobileModal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import type { IRemoveStakeholderAttr } from "./types";

import { AddUserModal } from "../../AddUserModal";
import { Alert } from "components/Alert";
import { Button } from "components/Button";
import type { IConfirmFn } from "components/ConfirmDialog";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Dropdown } from "components/Dropdown";
import { Hr } from "components/Layout";
import { Switch } from "components/Switch";
import { Text } from "components/Text";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import { ControlLabel } from "styles/styledComponents";
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

  const handleDeleteAccount = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm((): void => {
          void removeStakeholder();
        });
      },
    [removeStakeholder]
  );
  const handleLogoutClick = useCallback(
    (confirm: IConfirmFn): (() => void) =>
      (): void => {
        confirm((): void => {
          mixpanel.reset();
          location.assign("/logout");
        });
      },
    []
  );

  return (
    <Dropdown
      align={"left"}
      button={
        <Button icon={faUser} size={"md"}>
          {userName.split(" ")[0]}
        </Button>
      }
      id={"navbar-user-profile"}
    >
      <div className={"flex flex-column tl"}>
        <div className={"pa2"}>
          <Text bright={7} fw={7} mb={1}>
            {userName}
          </Text>
          <Text bright={7} mb={1}>
            {userEmail}
          </Text>
          {_.isUndefined(userIntPhone) ? undefined : (
            <Text bright={7} mb={1}>
              {t("navbar.mobile")}
              &nbsp;
              {userIntPhone}
            </Text>
          )}
          {userRole === undefined ? undefined : (
            <Text bright={7} mb={1}>
              {t("navbar.role")}
              &nbsp;
              {t(`userModal.roles.${_.camelCase(userRole)}`)}
            </Text>
          )}
          <Text bright={7}>
            {t("navbar.featurePreview")}
            &nbsp;
            <Switch
              checked={featurePreview}
              name={"featurePreview"}
              onChange={toggleFeaturePreview}
            />
          </Text>
        </div>
        <Hr />
        <Button disp={"block"} onClick={openTokenModal}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faKey} />
            &nbsp;
            {t("navbar.token")}
          </Text>
        </Button>
        <Button>
          <Link to={"/user/config"}>
            <Text bright={8}>
              <FontAwesomeIcon icon={faUserCog} />
              &nbsp;
              {t("navbar.notification")}
            </Text>
          </Link>
        </Button>
        <Button onClick={openMobileModal}>
          <Text bright={8}>
            <FontAwesomeIcon icon={faMobileAlt} />
            &nbsp;
            {t("navbar.mobile")}
          </Text>
        </Button>
        <Can do={"api_mutations_add_stakeholder_mutate"}>
          <Button onClick={openStakeholderModal}>
            <Text bright={8}>
              <FontAwesomeIcon icon={faUserPlus} />
              &nbsp;
              {t("navbar.user")}
            </Text>
          </Button>
          {isStakeholderModalOpen ? (
            <AddUserModal
              action={"add"}
              domainSuggestings={[]}
              editTitle={""}
              initialValues={{}}
              onClose={closeStakeholderModal}
              onSubmit={handleAddUserSubmit}
              open={true}
              suggestions={[]}
              title={t("navbar.user")}
              type={"user"}
            />
          ) : undefined}
        </Can>
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
            return (
              <Button onClick={handleDeleteAccount(confirm)}>
                <Text bright={8}>
                  <FontAwesomeIcon icon={faUserTimes} />
                  &nbsp;
                  {t("navbar.deleteAccount.text")}
                </Text>
              </Button>
            );
          }}
        </ConfirmDialog>
        <Hr />
        <ConfirmDialog title={t("navbar.logout")}>
          {(confirm): React.ReactNode => {
            return (
              <Button onClick={handleLogoutClick(confirm)}>
                <Text bright={8}>
                  <FontAwesomeIcon icon={faSignOutAlt} />
                  &nbsp;
                  {t("navbar.logout")}
                </Text>
              </Button>
            );
          }}
        </ConfirmDialog>
      </div>
      {isTokenModalOpen ? (
        <APITokenModal onClose={closeTokenModal} open={true} />
      ) : undefined}
      {isMobileModalOpen ? (
        <MobileModal onClose={closeMobileModal} />
      ) : undefined}
    </Dropdown>
  );
};
