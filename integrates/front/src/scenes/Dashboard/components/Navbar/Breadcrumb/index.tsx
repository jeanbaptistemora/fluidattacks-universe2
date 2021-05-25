import { useQuery } from "@apollo/client";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useLocation } from "react-router";
import { Link } from "react-router-dom";

import { AddOrganizationModal } from "./AddOrganizationModal";
import { GET_USER_ORGANIZATIONS } from "./queries";
import { SplitButton } from "./SplitButton";
import { BreadcrumbContainer, NavSplitButtonContainer } from "./styles";
import { stylizeBreadcrumbItem } from "./utils";

import { MenuItem } from "components/DropdownButton";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const Breadcrumb: React.FC = (): JSX.Element => {
  const { pathname } = useLocation();
  const { push } = useHistory();
  const { t } = useTranslation();

  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage
  );

  interface IUserOrgs {
    me: {
      organizations: { name: string }[];
      userEmail: string;
    };
  }
  const { data, refetch } = useQuery<IUserOrgs>(GET_USER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred fetching organizations for the navbar",
          error
        );
      });
    },
  });
  const organizationList =
    data === undefined
      ? [{ name: "" }]
      : _.sortBy(data.me.organizations, ["name"]);

  const handleOrganizationChange = useCallback(
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

  const path: string = escape(pathname);
  const pathData: string[] = path.split("/").slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;

  useEffect((): void => {
    void refetch();
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

  const [isOrganizationModalOpen, setOrganizationModalOpen] = useState(false);
  const openOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(true);
  }, []);
  const closeOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(false);
  }, []);

  return (
    <BreadcrumbContainer>
      <li>
        <NavSplitButtonContainer>
          <SplitButton
            content={
              <div className={"splitItems"}>
                <Can do={"api_mutations_create_organization_mutate"}>
                  <MenuItem
                    eventKey={""}
                    itemContent={t("sidebar.newOrganization.text")}
                    onClick={openOrganizationModal}
                  />
                  {isOrganizationModalOpen ? (
                    <AddOrganizationModal
                      onClose={closeOrganizationModal}
                      open={true}
                    />
                  ) : undefined}
                </Can>
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
    </BreadcrumbContainer>
  );
};
