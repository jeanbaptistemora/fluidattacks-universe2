import { useQuery } from "@apollo/client";
import { useCallback, useContext, useState } from "react";
import { openPopupWidget } from "react-calendly";
import { useRouteMatch } from "react-router-dom";

import { GET_GROUP_SERVICES } from "./queries";

import { authContext } from "utils/auth";
import { Logger } from "utils/logger";

interface IGetGroupServices {
  group: {
    name: string;
    serviceAttributes: string[];
  };
}

const useCalendly = (): {
  closeUpgradeModal: () => void;
  data: IGetGroupServices | undefined;
  isUpgradeOpen: boolean;
  openCalendly: () => void;
} => {
  const match = useRouteMatch<{ orgName: string; groupName: string }>(
    "/orgs/:orgName/groups/:groupName"
  );
  const groupName = match === null ? "" : match.params.groupName;

  const { userEmail, userName } = useContext(authContext);
  const [isUpgradeOpen, setIsUpgradeOpen] = useState(false);

  const { data } = useQuery<IGetGroupServices>(GET_GROUP_SERVICES, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("An error occurred fetching group services", error);
      });
    },
    skip: match === null,
    variables: { groupName },
  });

  const closeUpgradeModal = useCallback((): void => {
    setIsUpgradeOpen(false);
  }, []);

  const openCalendly = useCallback((): void => {
    if (data) {
      const { serviceAttributes } = data.group;

      if (
        serviceAttributes.includes("has_squad") &&
        serviceAttributes.includes("is_continuous")
      ) {
        openPopupWidget({
          prefill: {
            customAnswers: { a1: groupName },
            email: userEmail,
            name: userName,
          },
          url: "https://calendly.com/fluidattacks/talk-to-a-hacker",
        });
      } else {
        setIsUpgradeOpen(true);
      }
    }
  }, [data, groupName, userEmail, userName]);

  return { closeUpgradeModal, data, isUpgradeOpen, openCalendly };
};

export { useCalendly };
