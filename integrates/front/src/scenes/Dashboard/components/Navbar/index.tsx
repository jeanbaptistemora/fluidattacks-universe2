import { useQuery } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect } from "react";
import { withRouter } from "react-router";
import { Link, useHistory, useLocation } from "react-router-dom";
import { Field } from "redux-form";

import { SplitButton } from "./components/splitbutton";

import { Button } from "components/Button";
import { MenuItem } from "components/DropdownButton";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { stylizeBreadcrumbItem } from "scenes/Dashboard/components/Navbar/utils";
import { NewsWidget } from "scenes/Dashboard/components/NewsWidget";
import {
  BreadCrumb,
  Col100,
  Col25,
  NavBar,
  NavBarCollapse,
  NavBarForm,
  NavBarFormGroup,
  NavBarHeader,
  NavSplitButtonContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Text } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { alphaNumeric } from "utils/validations";

const NavbarComponent: React.FC = (): JSX.Element => {
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
  const { data, refetch: refetchOrganizationList } = useQuery(
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
      : // eslint-disable-next-line fp/no-mutating-methods, @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
        data.me.organizations.sort(
          (nameA: { name: string }, nameB: { name: string }): number =>
            nameA.name > nameB.name ? 1 : -1
        );

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
      <NavBar id={"navbar"}>
        <NavBarHeader>
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
        </NavBarHeader>
        <NavBarCollapse>
          <Col25>
            <TooltipWrapper
              id={"navbar.newsTooltip.id"}
              message={translate.t("navbar.newsTooltip")}
            >
              <NewsWidget />
            </TooltipWrapper>
          </Col25>
          <Col100>
            <Can do={"front_can_use_groups_searchbar"}>
              <li role={"presentation"}>
                <NavBarForm>
                  <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                    <NavBarFormGroup>
                      <Field
                        component={Text}
                        name={"projectName"}
                        placeholder={translate.t("navbar.searchPlaceholder")}
                        validate={[alphaNumeric]}
                      />
                      <Button
                        // eslint-disable-next-line react/forbid-component-props
                        className={"bg-sb b--sb outline-0"}
                        type={"submit"}
                      >
                        <FluidIcon icon={"search"} />
                      </Button>
                    </NavBarFormGroup>
                  </GenericForm>
                </NavBarForm>
              </li>
            </Can>
          </Col100>
        </NavBarCollapse>
      </NavBar>
    </React.StrictMode>
  );
};

const Navbar: React.ComponentClass = withRouter(NavbarComponent);

export { Navbar, NavbarComponent };
