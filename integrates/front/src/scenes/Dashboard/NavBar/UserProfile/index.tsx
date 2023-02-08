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
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback, useContext, useState } from "react";
import type { Context, FC, ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { Link, useHistory } from "react-router-dom";

import { AddUserModal } from "./AddUserModal";
import { MobileModal } from "./MobileModal";
import { REMOVE_STAKEHOLDER_MUTATION } from "./queries";
import type { IRemoveUserAttr } from "./types";

import { Alert } from "components/Alert";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { Dropdown } from "components/Dropdown";
import { Label } from "components/Input";
import { Hr } from "components/Layout";
import { Switch } from "components/Switch";
import { Text } from "components/Text";
import { APITokenModal } from "scenes/Dashboard/components/Navbar/UserProfile/APITokenModal";
import { useAddStakeholder } from "scenes/Dashboard/hooks";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import type { IFeaturePreviewContext } from "utils/featurePreview";
import { featurePreviewContext } from "utils/featurePreview";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IUserProfileProps {
  userRole: string | undefined;
}

const UserProfile: FC<IUserProfileProps> = ({
  userRole,
}: Readonly<IUserProfileProps>): JSX.Element => {
  const { userEmail, userName, userIntPhone } = useContext(authContext);
  const { t } = useTranslation();
  const { push } = useHistory();

  const { featurePreview, setFeaturePreview } = useContext(
    featurePreviewContext as Context<Required<IFeaturePreviewContext>>
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
    onCompleted: (mtResult: IRemoveUserAttr): void => {
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
        <Button disp={"block"} icon={faKey} onClick={openTokenModal}>
          {t("navbar.token")}
        </Button>
        <Link to={"/user/config"}>
          <Text>
            <Button disp={"block"} icon={faUserCog}>
              {t("navbar.notification")}
            </Button>
          </Text>
        </Link>
        <Button icon={faMobileAlt} onClick={openMobileModal}>
          {t("navbar.mobile")}
        </Button>
        <Can do={"api_mutations_add_stakeholder_mutate"}>
          <Button icon={faUserPlus} onClick={openStakeholderModal}>
            {t("navbar.user")}
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
            <Fragment>
              <Label>{t("navbar.deleteAccount.modal.warning")}</Label>
              <Alert>{t("navbar.deleteAccount.modal.text")}</Alert>
            </Fragment>
          }
          title={t("navbar.deleteAccount.text")}
        >
          {(confirm): React.ReactNode => {
            return (
              <Button icon={faUserTimes} onClick={handleDeleteAccount(confirm)}>
                {t("navbar.deleteAccount.text")}
              </Button>
            );
          }}
        </ConfirmDialog>
        <Hr />
        <ConfirmDialog title={t("navbar.logout")}>
          {(confirm): ReactNode => {
            return (
              <Button icon={faSignOutAlt} onClick={handleLogoutClick(confirm)}>
                {t("navbar.logout")}
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

export type { IUserProfileProps };
export { UserProfile };
