import type { IAuthResult } from "../..";
import { LOGGER } from "../../../logger";
import _ from "lodash";
import {
  AuthRequest,
  Prompt,
  ResponseType,
  fetchUserInfoAsync,
  makeRedirectUri,
} from "expo-auth-session";
import type { AuthSessionResult, DiscoveryDocument } from "expo-auth-session";
import {
  BITBUCKET_CLIENT_ID_DEV,
  BITBUCKET_CLIENT_ID_PROD,
} from "../../../constants";
// eslint-disable-next-line import/no-named-as-default -- Needed for correct usage of NativeConstants.appOwnership
import Constants, { AppOwnership } from "expo-constants";

const inExpoClient: boolean = Constants.appOwnership === AppOwnership.Expo;

const clientId: string = inExpoClient
  ? BITBUCKET_CLIENT_ID_DEV
  : BITBUCKET_CLIENT_ID_PROD;

const getRedirectUri: () => string = (): string =>
  makeRedirectUri({
    native: "com.fluidattacks.integrates://oauth2redirect/bitbucket",
    path: "oauth2redirect/bitbucket",
    useProxy: inExpoClient,
  });

const getDiscovery: () => DiscoveryDocument = (): DiscoveryDocument => ({
  authorizationEndpoint: "https://bitbucket.org/site/oauth2/authorize",
  tokenEndpoint: "https://bitbucket.org/site/oauth2/access_token",
  userInfoEndpoint: "https://api.bitbucket.org/2.0/user",
});

const authWithBitbucket: () => Promise<IAuthResult> = async (): Promise<IAuthResult> => {
  try {
    const discovery: DiscoveryDocument = getDiscovery();
    const request: AuthRequest = new AuthRequest({
      clientId,
      prompt: Prompt.SelectAccount,
      redirectUri: getRedirectUri(),
      responseType: ResponseType.Token,
      scopes: ["account", "email"],
      usePKCE: false,
    });

    const logInResult: AuthSessionResult = await request.promptAsync(
      discovery,
      { useProxy: inExpoClient }
    );

    if (logInResult.type === "success") {
      const { access_token: accessToken } = logInResult.params;

      /**
       * User properties returned by Bitbucket's API
       * @see https://developer.atlassian.com/bitbucket/api/2/reference/resource/user
       */
      interface IUserProps {
        account_id: string; // eslint-disable-line camelcase -- Required by auth API
        display_name: string; // eslint-disable-line camelcase -- Required by auth API
        links: {
          avatar: {
            href: string;
          };
        };
        username: string;
      }
      const userProps: IUserProps = (await fetchUserInfoAsync(
        { accessToken },
        { userInfoEndpoint: discovery.userInfoEndpoint }
      )) as IUserProps;

      /**
       * Accounts may have multiple associated emails but only one primary
       * @see https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/emails
       */
      interface IEmails {
        values: {
          email: string;
          is_primary: boolean; // eslint-disable-line camelcase -- Required by auth API
        }[];
      }
      const emailsResponse: Response = await fetch(
        "https://api.bitbucket.org/2.0/user/emails",
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );
      const {
        values: emails,
      }: IEmails = (await emailsResponse.json()) as IEmails;
      const { email: primaryEmail } = emails.find(
        (email: IEmails["values"][0]): boolean => email.is_primary
      ) as IEmails["values"][0];

      return {
        authProvider: "BITBUCKET",
        authToken: accessToken,
        type: "success",
        user: {
          email: primaryEmail,
          firstName: _.capitalize(userProps.username),
          fullName: _.startCase(userProps.display_name.toLowerCase()),
          photoUrl: userProps.links.avatar.href,
        },
      };
    }
  } catch (error: unknown) {
    LOGGER.error("Couldn't authenticate with Bitbucket", error);
  }

  return { type: "cancel" };
};

export { authWithBitbucket };
