import { faCaretDown, faUserCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import { DropdownMenu, MenuButton } from "../styles";
import { authContext } from "utils/auth";

const UserInfo = styled.p.attrs({
  className: "lh-title",
})``;

interface IUserProfileProps {
  userRole: string | undefined;
}

export const UserProfile: React.FC<IUserProfileProps> = ({
  userRole,
}: IUserProfileProps): JSX.Element => {
  const { userEmail, userName } = useContext(authContext);
  const { t } = useTranslation();

  const [isOpen, setOpen] = useState(false);
  const toggleDropdown = useCallback((): void => {
    setOpen((currentValue): boolean => !currentValue);
  }, []);

  return (
    <div>
      <MenuButton onClick={toggleDropdown}>
        <FontAwesomeIcon icon={faUserCircle} />
        <FontAwesomeIcon icon={faCaretDown} />
      </MenuButton>
      {isOpen ? (
        <DropdownMenu>
          <li>
            <UserInfo>
              <b>{userName}</b>
              <br />
              {userEmail}
              {userRole === undefined ? undefined : (
                <React.Fragment>
                  <br />
                  {t("sidebar.role")}&nbsp;
                  {t(`userModal.roles.${_.camelCase(userRole)}`)}
                </React.Fragment>
              )}
            </UserInfo>
          </li>
        </DropdownMenu>
      ) : undefined}
    </div>
  );
};
