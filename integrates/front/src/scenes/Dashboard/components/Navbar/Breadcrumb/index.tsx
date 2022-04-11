import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _, { capitalize } from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useHistory, useLocation } from "react-router-dom";

import { AddOrganizationModal } from "./AddOrganizationModal";
import { MenuItem } from "./MenuItem";
import { GET_FINDING_TITLE, GET_USER_ORGANIZATIONS } from "./queries";
import { SplitButton } from "./SplitButton";
import { BreadcrumbContainer, SplitItems } from "./styles";
import type { IFindingTitle, IUserOrgs } from "./types";
import { stylizeBreadcrumbItem } from "./utils";

import { NavbarButton } from "../styles";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const Breadcrumb: React.FC = (): JSX.Element => {
  const { pathname } = useLocation();
  const { action, goBack, push } = useHistory();
  const { t } = useTranslation();

  const [lastOrganization, setLastOrganization] = useStoredState(
    "organization",
    { name: "" },
    localStorage
  );
  const [lastGroup, setLastGroup] = useStoredState(
    "group",
    { name: "" },
    localStorage
  );

  function getCurrentGroupList(orgData: IUserOrgs): { name: string }[] {
    const currentOrg = _.find(orgData.me.organizations, [
      "name",
      lastOrganization.name,
    ]);

    return _.isUndefined(currentOrg)
      ? [{ name: "" }]
      : _.sortBy(currentOrg.groups, ["name"]);
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
      ? [{ groups: [], name: "" }]
      : _.sortBy(data.me.organizations, ["name"]);
  const groupList =
    data === undefined ? [{ name: "" }] : getCurrentGroupList(data);

  const [isOrgItemsOpen, setOrgItemsOpen] = useState(false);
  const showOrgItems = useCallback((): void => {
    setOrgItemsOpen(true);
  }, []);
  const hideOrgItems = useCallback((): void => {
    setOrgItemsOpen(false);
  }, []);

  const [isOrganizationModalOpen, setOrganizationModalOpen] = useState(false);
  const openOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(true);
    setOrgItemsOpen(false);
  }, []);
  const closeOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(false);
    void refetch();
  }, [refetch]);

  const isOrphanPath: boolean = useMemo(
    (): boolean => _.includes(["/user/config", "/todos"], pathname),
    [pathname]
  );
  const shouldDisplayGoBack: boolean = useMemo(
    (): boolean => action !== "POP" && isOrphanPath,
    [action, isOrphanPath]
  );

  const handleOrganizationChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastOrganization.name || isOrphanPath) {
        setLastOrganization({ name: eventKey });
        push(`/orgs/${eventKey}/groups`);
      }
      setOrgItemsOpen(false);
    },
    [lastOrganization.name, isOrphanPath, push, setLastOrganization]
  );

  const [isGroupItemsOpen, setGroupItemsOpen] = useState(false);
  const showGroupItems = useCallback((): void => {
    setGroupItemsOpen(true);
  }, []);
  const hideGroupItems = useCallback((): void => {
    setGroupItemsOpen(false);
  }, []);

  const handleGroupChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastGroup.name) {
        setLastGroup({ name: eventKey });
        push(`/orgs/${lastOrganization.name}/groups/${eventKey}/`);
      }
      setGroupItemsOpen(false);
    },
    [lastOrganization.name, lastGroup.name, push, setLastGroup]
  );

  const path: string = escape(pathname);
  const pathData: string[] = path.split("/").slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;
  /*
   * The searchbar can generate URLs with "/groups/" but not "/orgs/" before
   * it is redirected to the full URL
   */
  const pathGroup: string =
    path.includes("/orgs/") && path.includes("/groups/")
      ? pathData[2].toLowerCase()
      : "";
  if (pathGroup !== lastGroup.name) {
    setLastGroup({ name: pathGroup });
  }

  const pathBreadcrumbItems = pathData.slice(1);
  const findingAlias = ["drafts", "vulns"];
  const findingId = pathBreadcrumbItems.reduce(
    (id, item, index, arr): string => {
      const nextIndex = index + 1;

      return pathBreadcrumbItems.length > nextIndex &&
        findingAlias.includes(item)
        ? arr[nextIndex]
        : id;
    },
    ""
  );
  const { data: findingData } = useQuery<IFindingTitle>(GET_FINDING_TITLE, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding title", error);
      });
    },
    skip: _.isEmpty(findingId),
    variables: {
      findingId,
    },
  });

  const orgDropdown: JSX.Element = (
    <li>
      <SplitButton
        content={
          <SplitItems>
            <Can do={"api_mutations_add_organization_mutate"}>
              <MenuItem
                eventKey={""}
                itemContent={t("sidebar.newOrganization.text")}
                onClick={openOrganizationModal}
              />
            </Can>
            {organizationList.map(
              (organization: { name: string }): JSX.Element => (
                <MenuItem
                  eventKey={organization.name}
                  itemContent={capitalize(organization.name)}
                  key={organization.name}
                  onClick={handleOrganizationChange}
                />
              )
            )}
          </SplitItems>
        }
        id={"organizationList"}
        isOpen={isOrgItemsOpen}
        onClick={handleOrganizationChange}
        onHover={showOrgItems}
        onLeave={hideOrgItems}
        title={capitalize(pathOrganization)}
      />
    </li>
  );

  const groupDropdown: JSX.Element = (
    <li>
      <SplitButton
        content={
          <SplitItems>
            {groupList.map(
              (group: { name: string }): JSX.Element => (
                <MenuItem
                  eventKey={group.name}
                  itemContent={capitalize(group.name)}
                  key={group.name}
                  onClick={handleGroupChange}
                />
              )
            )}
          </SplitItems>
        }
        id={"groupList"}
        isOpen={isGroupItemsOpen}
        onClick={handleGroupChange}
        onHover={showGroupItems}
        onLeave={hideGroupItems}
        title={capitalize(pathGroup)}
      />
    </li>
  );

  const breadcrumbItems: JSX.Element[] = pathBreadcrumbItems.map(
    (item: string, index: number): JSX.Element => {
      const [, baseLink] = path.split("/");
      const link: string = pathData.slice(0, index + 2).join("/");
      const breadcrumbItem: string = findingAlias.includes(
        pathBreadcrumbItems[index - 1]
      )
        ? _.isUndefined(findingData)
          ? "-"
          : findingData.finding.title
        : item;

      if (breadcrumbItem === lastGroup.name) {
        return groupDropdown;
      }

      return (
        <li className={"pv2"} key={index.toString()}>
          <Link to={`/${baseLink}/${link}`}>
            {stylizeBreadcrumbItem(breadcrumbItem)}
          </Link>
        </li>
      );
    }
  );

  const fullBreadcrumb: JSX.Element[] = [orgDropdown, ...breadcrumbItems];

  return (
    <React.Fragment>
      {shouldDisplayGoBack ? (
        <NavbarButton onClick={goBack}>
          <span className={"fa-layers fa-fw"}>
            <FontAwesomeIcon icon={faArrowLeft} />
          </span>
        </NavbarButton>
      ) : undefined}
      <BreadcrumbContainer>{fullBreadcrumb}</BreadcrumbContainer>
      {isOrganizationModalOpen ? (
        <AddOrganizationModal onClose={closeOrganizationModal} open={true} />
      ) : undefined}
    </React.Fragment>
  );
};
