import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { Field } from "redux-form";

import { Breadcrumb } from "./Breadcrumb";
import { HelpWidget } from "./HelpWidget";
import { NewsWidget } from "./NewsWidget";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";
import { TechnicalInfo } from "./TechnicalInfo";
import { UserProfile } from "./UserProfile";

import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Can } from "utils/authz/Can";
import { Text } from "utils/forms/fields";
import { alphaNumeric } from "utils/validations";

interface INavbarProps {
  userRole: string | undefined;
}

export const Navbar: React.FC<INavbarProps> = ({
  userRole,
}: INavbarProps): JSX.Element => {
  const { push } = useHistory();
  const { t } = useTranslation();

  // Auxiliary Operations

  const handleSearchSubmit: (values: {
    projectName: string;
  }) => void = useCallback(
    (values: { projectName: string }): void => {
      const projectName: string = values.projectName.toLowerCase();
      if (!_.isEmpty(projectName)) {
        track("SearchGroup", { group: projectName });
        push(`/groups/${projectName}/vulns`);
      }
    },
    [push]
  );

  return (
    <React.StrictMode>
      <NavbarContainer id={"navbar"}>
        <NavbarHeader>
          <Breadcrumb />
        </NavbarHeader>
        <NavbarMenu>
          <Can do={"front_can_use_groups_searchbar"}>
            <li>
              <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                <Field
                  component={Text}
                  name={"projectName"}
                  placeholder={t("navbar.searchPlaceholder")}
                  validate={[alphaNumeric]}
                />
              </GenericForm>
            </li>
          </Can>
          <li>
            <TooltipWrapper
              id={"navbar.newsTooltip.id"}
              message={t("navbar.newsTooltip")}
            >
              <NewsWidget />
            </TooltipWrapper>
          </li>
          <li>
            <HelpWidget />
          </li>
          <li>
            <TechnicalInfo />
          </li>
          <li>
            <UserProfile userRole={userRole} />
          </li>
        </NavbarMenu>
      </NavbarContainer>
    </React.StrictMode>
  );
};
