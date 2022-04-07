import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _, { capitalize } from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useHistory, useLocation } from "react-router-dom";

import { AddOrganizationModal } from "./AddOrganizationModal";
import { MenuItem } from "./MenuItem";
import { GET_FINDING_TITLE, GET_USER_ORGANIZATIONS } from "./queries";
import { SplitButton } from "./SplitButton";
import {
  BreadcrumbContainer,
  NavSplitButtonContainer,
  SplitItems,
} from "./styles";
import type { IFindingTitle, IUserOrgs } from "./types";
import { stylizeBreadcrumbItem } from "./utils";

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

  const [isItemsOpen, setItemsOpen] = useState(false);
  const showItems = useCallback((): void => {
    setItemsOpen(true);
  }, []);
  const hideItems = useCallback((): void => {
    setItemsOpen(false);
  }, []);

  const [isOrganizationModalOpen, setOrganizationModalOpen] = useState(false);
  const openOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(true);
    setItemsOpen(false);
  }, []);
  const closeOrganizationModal: () => void = useCallback((): void => {
    setOrganizationModalOpen(false);
    void refetch();
  }, [refetch]);

  const handleOrganizationChange = useCallback(
    (eventKey: string): void => {
      if (eventKey !== lastOrganization.name) {
        setLastOrganization({ name: eventKey });
        push(`/orgs/${eventKey}/`);
      }
      setItemsOpen(false);
    },
    [lastOrganization.name, push, setLastOrganization]
  );

  const path: string = escape(pathname);
  const pathData: string[] = path.split("/").slice(2);
  const pathOrganization: string = path.includes("/orgs")
    ? pathData[0].toLowerCase()
    : lastOrganization.name;

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

      return (
        <li className={"pv2"} key={index.toString()}>
          <Link to={`/${baseLink}/${link}`}>
            {stylizeBreadcrumbItem(breadcrumbItem)}
          </Link>
        </li>
      );
    }
  );

  return (
    <React.Fragment>
      <BreadcrumbContainer>
        <li>
          <NavSplitButtonContainer>
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
              isOpen={isItemsOpen}
              onHover={showItems}
              onLeave={hideItems}
              title={capitalize(pathOrganization)}
            />
          </NavSplitButtonContainer>
        </li>
        {breadcrumbItems}
      </BreadcrumbContainer>
      {isOrganizationModalOpen ? (
        <AddOrganizationModal onClose={closeOrganizationModal} open={true} />
      ) : undefined}
    </React.Fragment>
  );
};
