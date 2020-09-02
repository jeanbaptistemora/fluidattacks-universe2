import { IAuthResult } from "../..";

const mockConstants: (values: Record<string, string>) => void = (
  values: Record<string, string>,
): void => {
  jest.doMock(
    "expo-constants",
    (): Record<string, {}> => {
      const constants: Record<string, {}> = jest.requireActual(
        "expo-constants",
      );

      return {
        ...constants,
        manifest: {
          ...(constants.default as Record<string, Record<string, string>>)
            .manifest,
          scheme: "com.fluidattacks.integrates",
        },
        ...values,
      };
    },
  );
};

describe("Google OAuth2 provider", (): void => {
  beforeEach((): void => {
    jest.resetModules();
    jest.mock("expo-auth-session");
  });

  it("should perform auth code grant flow", async (): Promise<void> => {
    mockConstants({ appOwnership: "standalone" });

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
      accessToken: "exchangedToken",
    });

    fetchDiscoveryAsync.mockResolvedValue({
      userInfoEndpoint: "https://openidconnect.googleapis.com/v1/userinfo",
    });

    fetchUserInfoAsync.mockResolvedValue({
      email: "test@fluidattacks.com",
      email_verified: true,
      family_name: "Doe",
      given_name: "John",
      locale: "en",
      name: "John Doe",
      picture: "https://lh3.googleusercontent.com/a-/something",
      sub: "000000000000000000000",
    });

    // tslint:disable-next-line: no-require-imports
    const { authWithGoogle } = require(".") as {
      authWithGoogle(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();
    expect(result)
    .toEqual({
      authProvider: "GOOGLE",
      authToken: "exchangedToken",
      type: "success",
      user: {
        email: "test@fluidattacks.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "Doe",
        photoUrl: "https://lh3.googleusercontent.com/a-/something",
      },
    });
  });

  it("should perform implicit flow", async (): Promise<void> => {
    mockConstants({ appOwnership: "expo" });

    const {
      AuthRequest,
      fetchDiscoveryAsync,
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

    fetchDiscoveryAsync.mockResolvedValue({
      userInfoEndpoint: "https://openidconnect.googleapis.com/v1/userinfo",
    });

    fetchUserInfoAsync.mockResolvedValue({
      email: "test@fluidattacks.com",
      email_verified: true,
      family_name: "Doe",
      given_name: "John",
      locale: "en",
      name: "John Doe",
      picture: "https://lh3.googleusercontent.com/a-/something",
      sub: "000000000000000000000",
    });

    // tslint:disable-next-line: no-require-imports
    const { authWithGoogle } = require(".") as {
      authWithGoogle(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();
    expect(result)
    .toEqual({
      authProvider: "GOOGLE",
      authToken: "accessToken",
      type: "success",
      user: {
        email: "test@fluidattacks.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "Doe",
        photoUrl: "https://lh3.googleusercontent.com/a-/something",
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
    const { authWithGoogle } = require(".") as {
      authWithGoogle(): Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();
    expect(result)
    .toEqual({ type: "cancel" });
  });
});
