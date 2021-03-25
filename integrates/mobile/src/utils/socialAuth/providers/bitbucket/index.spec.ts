/* eslint-disable @typescript-eslint/no-require-imports, @typescript-eslint/no-var-requires */
import type { FetchMockStatic } from "fetch-mock";

import type { IAuthResult } from "../..";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;

describe("Bitbucket OAuth2 provider", (): void => {
  it("should perform implicit flow", async (): Promise<void> => {
    expect.hasAssertions();

    jest.resetModules();
    jest.mock("expo-auth-session");

    const {
      AuthRequest,
      fetchUserInfoAsync,
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn().mockResolvedValue({
          errorCode: "",
          params: { access_token: "accessToken" }, // eslint-disable-line camelcase -- Required by auth API
          type: "success",
          url: "",
        }),
      })
    );

    fetchUserInfoAsync.mockResolvedValue({
      account_id: "", // eslint-disable-line camelcase -- Required by auth API
      display_name: "JOHN DOE", // eslint-disable-line camelcase -- Required by auth API
      links: {
        avatar: {
          href: "https://bitbucket.org/some/picture.png",
        },
      },
      username: "jdoe",
    });

    mockedFetch.mock("https://api.bitbucket.org/2.0/user/emails", {
      body: {
        values: [
          { email: "secondary@fluidattacks.com", is_primary: false }, // eslint-disable-line camelcase -- Required by auth API
          { email: "primary@fluidattacks.com", is_primary: true }, // eslint-disable-line camelcase -- Required by auth API
        ],
      },
      status: 200,
    });

    const { authWithBitbucket } = require(".") as {
      authWithBitbucket: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithBitbucket();

    expect(result).toStrictEqual({
      authProvider: "BITBUCKET",
      authToken: "accessToken",
      type: "success",
      user: {
        email: "primary@fluidattacks.com",
        firstName: "Jdoe",
        fullName: "John Doe",
        photoUrl: "https://bitbucket.org/some/picture.png",
      },
    });
  });

  it("should gracefully handle errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.resetModules();
    jest.mock("expo-auth-session");

    const { AuthRequest } = require("expo-auth-session") as Record<
      string,
      jest.Mock
    >;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn().mockRejectedValue(new Error()),
      })
    );

    const { authWithBitbucket } = require(".") as {
      authWithBitbucket: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithBitbucket();

    expect(result).toStrictEqual({ type: "cancel" });
  });
});
