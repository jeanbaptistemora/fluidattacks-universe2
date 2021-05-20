import {
  faCaretDown,
  faKey,
  faSignOutAlt,
  faUserCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import { reset } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { APITokenModal } from "../../APITokenModal";
import { DropdownButton, DropdownMenu, NavbarButton } from "../styles";
import { ConfirmDialog } from "components/ConfirmDialog";
import { TooltipWrapper } from "components/TooltipWrapper";
import { authContext } from "utils/auth";

const UserInfo = styled.p.attrs({
  className: "lh-title ph2",
})``;

const Divider = styled.hr.attrs({
  className: "mv2",
})``;

interface IUserProfileProps {
  userRole: string | undefined;
}

export const UserProfile: React.FC<IUserProfileProps> = ({
  userRole,
}: IUserProfileProps): JSX.Element => {
  const { userEmail, userName } = useContext(authContext);
  const { t } = useTranslation();

  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setDropdownOpen((currentValue): boolean => !currentValue);
  }, []);

  const [isTokenModalOpen, setTokenModalOpen] = useState(false);
  const openTokenModal = useCallback((): void => {
    setTokenModalOpen(true);
  }, []);
  const closeTokenModal = useCallback((): void => {
    setTokenModalOpen(false);
  }, []);

  return (
    <div>
      <NavbarButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faUserCircle} />
        <FontAwesomeIcon icon={faCaretDown} />
      </NavbarButton>
      {isDropdownOpen ? (
        <DropdownMenu>
          <li>
            <UserInfo>
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
            </UserInfo>
          </li>
          <Divider />
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
          <Divider />
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
