import { GraphQLError } from "graphql";
import { I18nextProvider } from "react-i18next";
import { MemoryRouter } from "react-router-native";
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { Provider as PaperProvider } from "react-native-paper";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { SIGN_IN_MUTATION } from "./queries";
import { WelcomeView } from ".";
import { act } from "react-dom/test-utils";
import { i18next } from "../../utils/translations/translate";
import { mount } from "enzyme";
import wait from "waait";

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock(
  "react-router-native",
  (): Record<string, unknown> => {
    const mockedRouter: Record<
      string,
      () => Record<string, unknown>
    > = jest.requireActual("react-router-native");

    return {
      ...mockedRouter,
      useHistory: (): Record<string, unknown> => ({
        ...mockedRouter.useHistory(),
        replace: mockHistoryReplace,
      }),
    };
  }
);

describe("WelcomeView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof WelcomeView).toStrictEqual("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              {
                pathname: "/Welcome",
                state: { user: { firstName: "John", fullName: "John Doe" } },
              },
            ]}
          >
            <MockedProvider addTypename={false}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("Hello John!");

    jest.clearAllMocks();
  });

  it("should auth against the API", async (): Promise<void> => {
    expect.hasAssertions();

    const signInMock: Readonly<MockedResponse> = {
      request: {
        query: SIGN_IN_MUTATION,
      },
      result: {
        data: {
          signIn: {
            sessionJwt: "s.ome.thing",
            success: true,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              {
                pathname: "/Welcome",
                state: {
                  user: {
                    email: "test@fluidattacks.com",
                    firstName: "John",
                    fullName: "John Doe",
                    lastName: "Doe",
                  },
                },
              },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[signInMock]}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Dashboard", {
      user: {
        email: "test@fluidattacks.com",
        firstName: "John",
        fullName: "John Doe",
        lastName: "Doe",
      },
    });

    jest.clearAllMocks();
  });

  it("should handle errors", async (): Promise<void> => {
    expect.hasAssertions();

    const signInMock: Readonly<MockedResponse> = {
      request: {
        query: SIGN_IN_MUTATION,
      },
      result: {
        errors: [new GraphQLError("Unexpected error")],
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              {
                pathname: "/Welcome",
                state: { user: { firstName: "John", fullName: "John Doe" } },
              },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[signInMock]}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Login");

    jest.clearAllMocks();
  });

  it("should handle unsuccesful api auth", async (): Promise<void> => {
    expect.hasAssertions();

    const signInMock: Readonly<MockedResponse> = {
      request: {
        query: SIGN_IN_MUTATION,
      },
      result: {
        data: {
          signIn: {
            sessionJwt: "",
            success: false,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              {
                pathname: "/Welcome",
                state: { user: { firstName: "John", fullName: "John Doe" } },
              },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[signInMock]}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Login");
  });

  jest.clearAllMocks();
});
