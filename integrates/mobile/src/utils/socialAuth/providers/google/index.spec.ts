/* eslint-disable @typescript-eslint/no-require-imports, @typescript-eslint/no-var-requires, camelcase */
import type { IAuthResult } from "../..";

const mockConstants: (values: Record<string, string>) => void = (
  values: Record<string, string>
): void => {
  jest.doMock(
    "expo-constants",
    (): Record<string, unknown> => {
      const constants: Record<string, unknown> = jest.requireActual(
        "expo-constants"
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
    }
  );
};

describe("Google OAuth2 provider", (): void => {
  it("should perform auth code grant flow", async (): Promise<void> => {
    expect.hasAssertions();

    jest.resetModules();
    jest.mock("expo-auth-session");
    mockConstants({ appOwnership: "standalone" });

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

    const { authWithGoogle } = require(".") as {
      authWithGoogle: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();

    expect(result).toStrictEqual({
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
    expect.hasAssertions();

    jest.resetModules();
    jest.mock("expo-auth-session");
    mockConstants({ appOwnership: "expo" });

    const {
      AuthRequest,
      fetchDiscoveryAsync,
      fetchUserInfoAsync,
    } = require("expo-auth-session") as Record<string, jest.Mock>;
    AuthRequest.mockImplementation(
      (): Record<string, jest.Mock> => ({
        promptAsync: jest.fn().mockResolvedValue({
          errorCode: "",
          params: { access_token: "accessToken" },
          type: "success",
          url: "",
        }),
      })
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

    const { authWithGoogle } = require(".") as {
      authWithGoogle: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();

    expect(result).toStrictEqual({
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

    const { authWithGoogle } = require(".") as {
      authWithGoogle: () => Promise<IAuthResult>;
    };
    const result: IAuthResult = await authWithGoogle();

    expect(result).toStrictEqual({ type: "cancel" });
  });
});
