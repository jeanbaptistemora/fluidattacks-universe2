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
import {
  GET_FINDING_TITLE,
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "./queries";
import { SplitButton } from "./SplitButton";
import { BreadcrumbContainer, SplitItems } from "./styles";
import type {
  IFindingTitle,
  IUserOrganizationGroupNames,
  IUserOrgs,
  IUserTags,
} from "./types";
import { stylizeBreadcrumbItem } from "./utils";

import { Button } from "components/Button";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import type { IGetOrganizationId } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/types";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const Breadcrumb: React.FC = (): JSX.Element => {
  const { pathname } = useLocation();
  const { goBack, push } = useHistory();
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
  const [lastPortfolio, setLastPortfolio] = useStoredState(
    "portfolio",
    { name: "" },
    localStorage
  );

  const path: string = escape(pathname);

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

  const { data: basicData } = useQuery<IGetOrganizationId>(
    GET_ORGANIZATION_ID,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred fetching organization ID", error);
        });
      },
      skip: lastOrganization.name === "",
      variables: {
        organizationName: lastOrganization.name.toLowerCase(),
      },
    }
  );

  const { data: portfolioData } = useQuery<IUserTags>(GET_USER_TAGS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching portfolios", error);
      });
    },
    skip: basicData === undefined,
    variables: {
      organizationId: basicData?.organizationId.id,
    },
  });

  const { data: groupNamesData } = useQuery<IUserOrganizationGroupNames>(
    GET_ORGANIZATION_GROUP_NAMES,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred fetching portfolios", error);
        });
      },
      variables: {
        organizationId: lastOrganization.name.toLowerCase(),
      },
    }
  );

  const organizationList =
    data === undefined
      ? [{ groups: [], name: "" }]
      : _.sortBy(data.me.organizations, ["name"]);
  const groupList =
    groupNamesData === undefined
      ? [{ name: "" }]
      : groupNamesData.organization.groups;
  const portfolioList =
    portfolioData === undefined
      ? [{ name: "" }]
      : _.sortBy(portfolioData.me.tags, ["name"]);

  const [isOrgItemsOpen, setIsOrgItemsOpen] = useState(false);
  const showOrgItems = useCallback((): void => {
    setIsOrgItemsOpen(true);
  }, []);
  const hideOrgItems = useCallback((): void => {
    setIsOrgItemsOpen(false);
  }, []);

  const [isOrganizationModalOpen, setIsOrganizationModalOpen] = useState(false);
  const openOrganizationModal: () => void = useCallback((): void => {
    setIsOrganizationModalOpen(true);
    setIsOrgItemsOpen(false);
  }, []);
  const closeOrganizationModal: () => void = useCallback((): void => {
    setIsOrganizationModalOpen(false);
    void refetch();
  }, [refetch]);

  const shouldDisplayGoBack: boolean = useMemo(
    (): boolean =>
      _.includes(
        ["/user/config", "/todos/vulns", "/todos/drafts", "/todos/reattacks"],
        pathname
      ),
    [pathname]
  );

  const handleOrganizationChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastOrganization.name || shouldDisplayGoBack) {
        setLastOrganization({ name: eventKey });
        push(`/orgs/${eventKey}/groups`);
      }
      setIsOrgItemsOpen(false);
    },
    [lastOrganization.name, shouldDisplayGoBack, push, setLastOrganization]
  );

  const [isGroupItemsOpen, setIsGroupItemsOpen] = useState(false);
  const showGroupItems = useCallback((): void => {
    setIsGroupItemsOpen(true);
  }, []);
  const hideGroupItems = useCallback((): void => {
    setIsGroupItemsOpen(false);
  }, []);

  const handleGroupChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastGroup.name) {
        setLastGroup({ name: eventKey });
        push(`/orgs/${lastOrganization.name}/groups/${eventKey}/`);
      }
      setIsGroupItemsOpen(false);
    },
    [lastOrganization.name, lastGroup.name, push, setLastGroup]
  );

  const [isPortfolioItemsOpen, setIsPortfolioItemsOpen] = useState(false);
  const showPortfolioItems = useCallback((): void => {
    setIsPortfolioItemsOpen(true);
  }, []);
  const hidePortfolioItems = useCallback((): void => {
    setIsPortfolioItemsOpen(false);
  }, []);

  const handlePortfolioChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastPortfolio.name) {
        setLastPortfolio({ name: eventKey });
        push(`/orgs/${lastOrganization.name}/portfolios/${eventKey}/`);
      }
      setIsPortfolioItemsOpen(false);
    },
    [lastOrganization.name, lastPortfolio.name, push, setLastPortfolio]
  );

  const pathData: string[] = path.split("/").slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;
  if (pathOrganization !== lastOrganization.name) {
    setLastOrganization({ name: pathOrganization });
  }
  /*
   * The searchbar can generate URLs with "/groups/" but not "/orgs/" before
   * it is redirected to the full URL
   */
  const pathGroup: string =
    path.includes("/orgs/") &&
    path.includes("/groups/") &&
    !path.endsWith("/groups/")
      ? pathData[2].toLowerCase()
      : "";
  if (pathGroup !== lastGroup.name) {
    setLastGroup({ name: pathGroup });
  }
  const pathPortfolio: string =
    path.includes("/orgs/") && path.includes("/portfolios/")
      ? pathData[2].toLowerCase()
      : "";
  if (pathPortfolio !== lastPortfolio.name) {
    setLastPortfolio({ name: pathPortfolio });
  }

  const pathBreadcrumbItems = pathData.slice(0);
  const findingAlias = ["drafts", "vulns"];
  const findingId = pathBreadcrumbItems.reduce(
    (id, item, index, arr): string => {
      const nextIndex = index + 1;

      return pathBreadcrumbItems.length > nextIndex &&
        findingAlias.includes(item) &&
        arr.length > nextIndex + 1
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

  const portfolioDropdown: JSX.Element = (
    <li>
      <SplitButton
        content={
          <SplitItems>
            {portfolioList.map(
              (portfolio: { name: string }): JSX.Element => (
                <MenuItem
                  eventKey={portfolio.name}
                  itemContent={capitalize(portfolio.name)}
                  key={portfolio.name}
                  onClick={handlePortfolioChange}
                />
              )
            )}
          </SplitItems>
        }
        id={"portfolioList"}
        isOpen={isPortfolioItemsOpen}
        onClick={handlePortfolioChange}
        onHover={showPortfolioItems}
        onLeave={hidePortfolioItems}
        title={capitalize(pathPortfolio)}
      />
    </li>
  );

  const breadcrumbItems: JSX.Element[] = pathBreadcrumbItems.map(
    (item: string, index: number): JSX.Element => {
      const [, baseLink] = path.split("/");
      const link: string = pathData.slice(0, index + 1).join("/");

      function getBreadcrumItem(): string {
        if (findingAlias.includes(pathBreadcrumbItems[index - 1])) {
          if (_.isUndefined(findingData)) {
            return "-";
          }

          return findingData.finding.title;
        }

        return item;
      }

      const breadcrumbItem: string = getBreadcrumItem();

      if (breadcrumbItem === lastOrganization.name && index === 0) {
        return orgDropdown;
      }
      if (breadcrumbItem === lastGroup.name) {
        return groupDropdown;
      }
      if (breadcrumbItem === lastPortfolio.name) {
        return portfolioDropdown;
      }

      return (
        <li className={"pv2"} key={breadcrumbItem}>
          <Link to={`/${baseLink}/${link}`}>
            {stylizeBreadcrumbItem(breadcrumbItem)}
          </Link>
        </li>
      );
    }
  );

  return (
    <React.Fragment>
      {shouldDisplayGoBack ? (
        <Button onClick={goBack} size={"sm"}>
          <FontAwesomeIcon color={"#2e2e38"} icon={faArrowLeft} />
        </Button>
      ) : undefined}
      <BreadcrumbContainer>
        {breadcrumbItems.length === 0 ? orgDropdown : breadcrumbItems}
      </BreadcrumbContainer>
      {isOrganizationModalOpen ? (
        <AddOrganizationModal onClose={closeOrganizationModal} open={true} />
      ) : undefined}
    </React.Fragment>
  );
};
