import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Provider as PaperProvider } from "react-native-paper";
import { MemoryRouter } from "react-router-native";

import { i18next } from "../../utils/translations/translate";

import { WelcomeView } from "./index";
import { SIGN_IN_MUTATION } from "./queries";

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Dictionary => {
  const mockedRouter: Dictionary<() => Dictionary> = jest.requireActual("react-router-native");

  return {
    ...mockedRouter,
    useHistory: (): Dictionary => ({
      ...mockedRouter.useHistory(),
      replace: mockHistoryReplace,
    }),
  };
});

describe("WelcomeView", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
  });

  it("should return a function", (): void => {
    expect(typeof (WelcomeView))
      .toEqual("function");
  });

  it("should render", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{
            pathname: "/Welcome",
            state: { user: { firstName: "John", fullName: "John Doe" } },
          }]}>
            <MockedProvider addTypename={false}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("Hello John!");
  });

  it("should auth against the API", async (): Promise<void> => {

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
          <MemoryRouter initialEntries={[{
            pathname: "/Welcome",
            state: {
              user: {
                email: "test@fluidattacks.com",
                firstName: "John",
                fullName: "John Doe",
                lastName: "Doe",
              },
            },
          }]}>
            <MockedProvider mocks={[signInMock]} addTypename={false}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Dashboard", {
        user: {
          email: "test@fluidattacks.com",
          firstName: "John",
          fullName: "John Doe",
          lastName: "Doe",
        },
      });
  });

  it("should handle errors", async (): Promise<void> => {

    const signInMock: Readonly<MockedResponse> = {
      request: {
        query: SIGN_IN_MUTATION,
      },
      result: {
        errors: [
          new GraphQLError("Unexpected error"),
        ],
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter initialEntries={[{
            pathname: "/Welcome",
            state: { user: { firstName: "John", fullName: "John Doe" } },
          }]}>
            <MockedProvider mocks={[signInMock]} addTypename={false}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Login");
  });

  it("should handle unsuccesful api auth", async (): Promise<void> => {

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
          <MemoryRouter initialEntries={[{
            pathname: "/Welcome",
            state: { user: { firstName: "John", fullName: "John Doe" } },
          }]}>
            <MockedProvider mocks={[signInMock]} addTypename={false}>
              <WelcomeView />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
    expect(mockHistoryReplace)
      .toHaveBeenCalledWith("/Login");
  });
});
