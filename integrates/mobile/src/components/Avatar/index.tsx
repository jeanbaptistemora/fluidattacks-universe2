import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import type { GraphQLError } from "graphql";
import React from "react";
import { Avatar as PaperAvatar } from "react-native-paper";
import { useHistory } from "react-router-native";

import { REMOVE_ACCOUNT_MUTATION } from "./queries";
import type { IRemoveAccountResult } from "./types";

import { LOGGER } from "../../utils/logger";
import { useSessionToken } from "../../utils/sessionToken/context";
import type { IAuthState } from "../../utils/socialAuth";
import { logout } from "../../utils/socialAuth";

/** User avatar */
interface IAvatarProps {
  photoUrl?: string; // eslint-disable-line react/require-default-props
  size: number;
  userName: string;
}

const maxInitials: number = 2;
const getInitials: (name: string) => string = (name: string): string =>
  // eslint-disable-next-line fp/no-mutating-methods
  name
    .split(" ")
    .splice(0, maxInitials)
    .map((word: string): string => word.charAt(0).toUpperCase())
    .join("");

const Avatar: React.FC<IAvatarProps> = ({
  photoUrl,
  size,
  userName,
}: IAvatarProps): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { user } = history.location.state as IAuthState;
  const [, setSessionToken] = useSessionToken();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_removeAccount, { client }] = useMutation(REMOVE_ACCOUNT_MUTATION, {
    onCompleted: async (mtResult: IRemoveAccountResult): Promise<void> => {
      if (mtResult.removeStakeholder.success) {
        client.stop();
        await client.clearStore();
        await logout(setSessionToken);
        history.replace("/Login");
      } else {
        history.replace("/Dashboard", { user });
      }
    },
    onError: (removeError: ApolloError): void => {
      removeError.graphQLErrors.forEach((error: GraphQLError): void => {
        LOGGER.error("An error occurred while deleting account", error);
      });
      history.replace("/Dashboard", { user });
    },
  });

  return (
    <React.StrictMode>
      {photoUrl === undefined ? (
        <PaperAvatar.Text label={getInitials(userName)} size={size} />
      ) : (
        <PaperAvatar.Image size={size} source={{ uri: photoUrl }} />
      )}
    </React.StrictMode>
  );
};

export { Avatar };
