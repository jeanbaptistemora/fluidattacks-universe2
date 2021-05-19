import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useEffect } from "react";
import { Link, useHistory, useLocation } from "react-router-dom";
import { Field } from "redux-form";

import { HelpWidget } from "./HelpWidget";
import { NewsWidget } from "./NewsWidget";
import { SplitButton } from "./SplitButton";
import { NavbarContainer, NavbarHeader, NavbarMenu } from "./styles";

import { MenuItem } from "components/DropdownButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { stylizeBreadcrumbItem } from "scenes/Dashboard/components/Navbar/utils";
import { BreadCrumb, NavSplitButtonContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Text } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { alphaNumeric } from "utils/validations";

export const Navbar: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { pathname } = useLocation();
  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage
  );

  const path: string = escape(pathname);
  const pathData: string[] = path.split("/").slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;

  // GraphQL operations
  interface IUserOrgs {
    me: {
      organizations: { name: string }[];
      userEmail: string;
    };
  }

  const { data, refetch: refetchOrganizationList } = useQuery<IUserOrgs>(
    GET_USER_ORGANIZATIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred fetching organizations for the navbar",
            error
          );
        });
      },
    }
  );

  // Auxiliary Operations
  const handleOrganizationChange: (eventKey: string) => void = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastOrganization.name) {
        setLastOrganization({ name: eventKey });
        push(`/orgs/${eventKey}/`);
      }
      document
        .getElementsByClassName("splitItems")[0]
        .setAttribute("style", "display:none;");
    },
    [lastOrganization.name, push, setLastOrganization]
  );
  const handleOrganizationClick: () => void = useCallback((): void => {
    push(`/orgs/${lastOrganization.name}/`);
  }, [lastOrganization.name, push]);

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

  const HANDLE_BLUR_EVENT_TIMEOUT: number = 250;
  const handleBlurEvent: (event: FocusEvent) => void = (
    event: FocusEvent
  ): void => {
    const child: HTMLElement = event.target as HTMLElement;
    const element: HTMLElement = child.parentNode as HTMLElement;
    setTimeout((): void => {
      element.setAttribute("style", "display:none;");
    }, HANDLE_BLUR_EVENT_TIMEOUT);
    child.removeEventListener("blur", (): void => undefined);
  };
  const showItems: () => void = useCallback((): void => {
    const element: Element = document.querySelector(".splitItems") as Element;
    const child: HTMLElement = element.firstChild as HTMLElement;
    const elementStyle: CSSStyleDeclaration = window.getComputedStyle(element);
    const displayValue: string = elementStyle.getPropertyValue("display");
    if (displayValue === "none") {
      element.setAttribute("style", "display:block;");
      child.addEventListener("blur", handleBlurEvent);
      child.focus();
    }
  }, []);

  // Render Elements
  const organizationList: { name: string }[] =
    _.isEmpty(data) || _.isUndefined(data)
      ? [{ name: "" }]
      : _.sortBy(data.me.organizations, ["name"]);

  useEffect((): void => {
    void refetchOrganizationList();
    setLastOrganization({ name: pathOrganization });
    // Annotation needed as adding the dependencies creates a memory leak
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathOrganization]);

  const breadcrumbItems: JSX.Element[] = pathData.slice(1).map(
    (item: string, index: number): JSX.Element => {
      const [, baseLink] = path.split("/");
      const link: string = pathData.slice(0, index + 2).join("/");

      return (
        <li key={index.toString()}>
          <Link to={`/${baseLink}/${link}`}>{stylizeBreadcrumbItem(item)}</Link>
        </li>
      );
    }
  );

  return (
    <React.StrictMode>
      <NavbarContainer id={"navbar"}>
        <NavbarHeader>
          <BreadCrumb>
            <li>
              <NavSplitButtonContainer>
                <SplitButton
                  content={
                    <div className={"splitItems"}>
                      {organizationList.map(
                        (organization: { name: string }): JSX.Element => (
                          <MenuItem
                            eventKey={organization.name}
                            itemContent={organization.name}
                            key={organization.name}
                            onClick={handleOrganizationChange}
                          />
                        )
                      )}
                    </div>
                  }
                  id={"organizationList"}
                  onClick={handleOrganizationClick}
                  onClickIcon={showItems}
                  title={pathOrganization}
                />
              </NavSplitButtonContainer>
            </li>
            {breadcrumbItems}
          </BreadCrumb>
        </NavbarHeader>
        <NavbarMenu>
          <Can do={"front_can_use_groups_searchbar"}>
            <li>
              <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                <Field
                  component={Text}
                  name={"projectName"}
                  placeholder={translate.t("navbar.searchPlaceholder")}
                  validate={[alphaNumeric]}
                />
              </GenericForm>
            </li>
          </Can>
          <li>
            <TooltipWrapper
              id={"navbar.newsTooltip.id"}
              message={translate.t("navbar.newsTooltip")}
            >
              <NewsWidget />
            </TooltipWrapper>
          </li>
          <li>
            <HelpWidget />
          </li>
        </NavbarMenu>
      </NavbarContainer>
    </React.StrictMode>
  );
};
