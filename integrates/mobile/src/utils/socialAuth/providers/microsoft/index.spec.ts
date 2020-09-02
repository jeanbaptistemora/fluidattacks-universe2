import { IAuthResult } from "../..";

describe("Microsoft OAuth2 provider", (): void => {
  beforeEach((): void => {
    jest.resetModules();
    jest.mock("expo-auth-session");
  });

  it("should perform auth code grant flow", async (): Promise<void> => {
    const {
      AuthRequest,
      exchangeCodeAsync,
      fetchDiscoveryAsync,
      fetchUserInfoAsync,
      // tslint:disable-next-line: no-require-imports
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn()
        .mockResolvedValue({
          errorCode: "",
          params: { code: "codeToExchange" },
          type: "success",
          url: "",
        }),
      }),
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
      family_name: "DOE",
      given_name: "JOHN",
      name: "JOHN DOE",
    });

    // tslint:disable-next-line: no-require-imports
    const { authWithMicrosoft } = require(".") as {
      authWithMicrosoft(): Promise<IAuthResult>;
    };

    expect(await authWithMicrosoft())
    .toEqual({
      authProvider: "MICROSOFT",
      authToken: "exchangedIdToken",
      type: "success",
      user: {
        email: "personal@domain.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "DOE",
      },
    });

    fetchUserInfoAsync.mockResolvedValue({
      family_name: "DOE",
      given_name: "JOHN",
      name: "JOHN DOE",
      upn: "business@domain.com",
    });

    expect(await authWithMicrosoft())
    .toEqual({
      authProvider: "MICROSOFT",
      authToken: "exchangedIdToken",
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
    const { authWithMicrosoft } = require(".") as {
      authWithMicrosoft(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithMicrosoft();
    expect(result)
    .toEqual({ type: "cancel" });
  });
});
