import { FetchMockStatic } from "fetch-mock";

import { IAuthResult } from "../..";

const mockedFetch: FetchMockStatic = fetch as typeof fetch & FetchMockStatic;

describe("Bitbucket OAuth2 provider", (): void => {
  beforeEach((): void => {
    jest.resetModules();
    jest.mock("expo-auth-session");
  });

  it("should perform implicit flow", async (): Promise<void> => {
    const {
      AuthRequest,
      fetchUserInfoAsync,
      // tslint:disable-next-line: no-require-imports
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn()
        .mockResolvedValue({
          errorCode: "",
          params: { access_token: "accessToken" },
          type: "success",
          url: "",
        }),
      }),
    );

    fetchUserInfoAsync.mockResolvedValue({
      account_id: "",
      display_name: "JOHN DOE",
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
          { email: "secondary@fluidattacks.com", is_primary: false },
          { email: "primary@fluidattacks.com", is_primary: true },
        ],
      },
      status: 200,
    });

    // tslint:disable-next-line: no-require-imports
    const { authWithBitbucket } = require(".") as {
      authWithBitbucket(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithBitbucket();
    expect(result)
    .toEqual({
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
    const {
      AuthRequest,
      // tslint:disable-next-line: no-require-imports
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn()
        .mockRejectedValue(new Error()),
      }),
    );

    // tslint:disable-next-line: no-require-imports
    const { authWithBitbucket } = require(".") as {
      authWithBitbucket(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithBitbucket();
    expect(result)
    .toEqual({ type: "cancel" });
  });
});
