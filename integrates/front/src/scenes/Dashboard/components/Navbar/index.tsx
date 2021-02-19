import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { withRouter } from "react-router";
import { Link, useHistory, useLocation } from "react-router-dom";
import { Field } from "redux-form";
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

import { Button } from "components/Button";
import { MenuItem } from "components/DropdownButton";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { stylizeBreadcrumbItem } from "scenes/Dashboard/components/Navbar/utils";
import { NewsWidget } from "scenes/Dashboard/components/NewsWidget";
import { Can } from "utils/authz/Can";
import { Text } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { alphaNumeric } from "utils/validations";
import { SplitButton } from "./components/splitbutton";

export const navbarComponent: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { pathname } = useLocation();
  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage,
  );

  const path: string = escape(pathname);
  const pathData: string[] = path.split("/")
    .slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;

  // GraphQL operations
  const { data, refetch: refetchOrganizationList } = useQuery(
    GET_USER_ORGANIZATIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning(
            "An error occurred fetching organizations for the navbar",
            error,
          );
        });
      },
    },
  );

  // Auxiliary Operations
  const handleOrganizationChange: (
    eventKey: string,
  ) => void = (eventKey: string): void => {
    if (eventKey !== lastOrganization.name) {
      setLastOrganization({ name: eventKey });
      push(`/orgs/${eventKey}/`);
    }
    document.getElementsByClassName("splitItems")[0]
      .setAttribute("style", "display:none;");
  };
  const handleOrganizationClick: () => void = () => {
    push(`/orgs/${lastOrganization.name}/`);
  };
  const handleSearchSubmit: (values: {
    projectName: string;
  }) => void = (values: { projectName: string }): void => {
    const projectName: string = values.projectName.toLowerCase();
    if (!_.isEmpty(projectName)) {
      push(`/groups/${projectName}/indicators`);
    }
  };
  const handleBlurEvent: (event: FocusEvent) => void = (event: FocusEvent): void => {
    const child: HTMLElement = event.target as HTMLElement;
    const element: HTMLElement = child.parentNode as HTMLElement;
    setTimeout(
      () => {
        element.setAttribute("style", "display:none;");
      },
      250,
    );
    child.removeEventListener("blur", () => undefined);
  };
  const showItems: () => void = () => {
    const element: Element = document.querySelector(".splitItems") as Element;
    const child: HTMLElement = element.firstChild as HTMLElement;
    const elementStyle: CSSStyleDeclaration = window.getComputedStyle(element);
    const displayValue: string = elementStyle.getPropertyValue("display");
    if (displayValue === "none") {
      element.setAttribute("style", "display:block;");
      child.addEventListener("blur", handleBlurEvent);
      child.focus();
    }
  };

  // Render Elements
  const organizationList: Array<{ name: string }> =
    _.isEmpty(data) || _.isUndefined(data)
      ? [{ name: "" }]
      : data.me.organizations.sort((a: { name: string }, b: { name: string }) =>
          a.name > b.name ? 1 : -1,
        );

  React.useEffect((): void => {
    refetchOrganizationList();
    setLastOrganization({ name: pathOrganization });
  },              [pathOrganization]);

  const breadcrumbItems: JSX.Element[] = pathData
    .slice(1)
    .map((item: string, index: number) => {
      const baseLink: string = path.split("/")[1];
      const link: string = pathData.slice(0, index + 2)
        .join("/");

      return (
        <li key={index}>
          <Link to={`/${baseLink}/${link}`}>{stylizeBreadcrumbItem(item)}</Link>
        </li>
      );
    });

  return (
    <React.StrictMode>
      <NavBar id={"navbar"}>
        <NavBarHeader>
          <BreadCrumb>
            <li>
              <NavSplitButtonContainer>
                <SplitButton
                  id={"organizationList"}
                  onClick={handleOrganizationClick}
                  onClickIcon={showItems}
                  title={pathOrganization}
                  content={
                    <div className={"splitItems"}>
                      {organizationList.map((organization: { name: string }) => (
                        <MenuItem
                          eventKey={organization.name}
                          key={organization.name}
                          itemContent={organization.name}
                          onClick={handleOrganizationChange}
                        />
                      ))}
                    </div>
                  }
                />
              </NavSplitButtonContainer>
            </li>
            {breadcrumbItems}
          </BreadCrumb>
        </NavBarHeader>
        <NavBarCollapse>
          <Col25>
            <TooltipWrapper
              id={"navbar.news_tooltip.id"}
              message={translate.t("navbar.news_tooltip")}
            >
            <NewsWidget />
            </TooltipWrapper>
          </Col25>
          <Col100>
            <Can do="front_can_use_groups_searchbar">
              <li role="presentation">
                <NavBarForm>
                  <GenericForm name={"searchBar"} onSubmit={handleSearchSubmit}>
                    <NavBarFormGroup>
                      <Field
                        component={Text}
                        name={"projectName"}
                        placeholder={translate.t("navbar.searchPlaceholder")}
                        validate={[alphaNumeric]}
                      />
                      <Button className={"bg-sb b--sb outline-0"} type={"submit"}>
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

const navbar: React.ComponentClass = withRouter(navbarComponent);

export { navbar as Navbar };
