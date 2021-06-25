/* eslint-disable @typescript-eslint/no-require-imports, @typescript-eslint/no-var-requires */
import type { IAuthResult } from "../..";

describe("Microsoft OAuth2 provider", (): void => {
  it("should perform auth code grant flow", async (): Promise<void> => {
    expect.hasAssertions();

    jest.resetModules();
    jest.mock("expo-auth-session");
    const {
      AuthRequest,
      exchangeCodeAsync,
      fetchDiscoveryAsync,
      fetchUserInfoAsync,
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn().mockResolvedValue({
          errorCode: "",
          params: { code: "codeToExchange" },
          type: "success",
          url: "",
        }),
      })
    );

    exchangeCodeAsync.mockResolvedValue({
      accessToken: "exchangedAccessToken",
      idToken: "exchangedIdToken",
    });

    fetchDiscoveryAsync.mockResolvedValue({
      userInfoEndpoint:
        "https://login.microsoftonline.com/common/openid/userinfo",
    });

    fetchUserInfoAsync.mockResolvedValue({
      email: "personal@domain.com",
      family_name: "DOE", // eslint-disable-line camelcase -- Required by auth API
      given_name: "JOHN", // eslint-disable-line camelcase -- Required by auth API
      name: "JOHN DOE",
    });

    const { authWithMicrosoft } = require(".") as {
      authWithMicrosoft: () => Promise<IAuthResult>;
    };

    expect(await authWithMicrosoft()).toStrictEqual({
      authProvider: "MICROSOFT",
      authToken: "exchangedAccessToken",
      type: "success",
      user: {
        email: "personal@domain.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "DOE",
      },
    });

    fetchUserInfoAsync.mockResolvedValue({
      family_name: "DOE", // eslint-disable-line camelcase -- Required by auth API
      given_name: "JOHN", // eslint-disable-line camelcase -- Required by auth API
      name: "JOHN DOE",
      upn: "business@domain.com",
    });

    expect(await authWithMicrosoft()).toStrictEqual({
      authProvider: "MICROSOFT",
      authToken: "exchangedAccessToken",
      type: "success",
      user: {
        email: "business@domain.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "DOE",
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

    const { authWithMicrosoft } = require(".") as {
      authWithMicrosoft: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithMicrosoft();

    expect(result).toStrictEqual({ type: "cancel" });
  });
});
