import React from "react";
import { Provider as ThemeProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import renderer, { ReactTestRenderer } from "react-test-renderer";

import { theme } from "../../app";

import { ILoginProps, LoginView } from "./index";

/** Mocked types for react-native */
interface IMockedRN {
  Platform: { OS: string };
}

jest.mock("react-native", (): IMockedRN => {
  const mockedRN: IMockedRN = jest.requireActual("react-native") as IMockedRN;
  mockedRN.Platform.OS = "test-env";

  return mockedRN;
});

describe("LoginView", (): void => {
  it("should render", (): void => {

    const mockProps: ILoginProps = {
      history: {
        action: "PUSH",
        block: (): (() => void) => (): void => undefined,
        createHref: (): string => "",
        go: (): void => undefined,
        goBack: (): void => undefined,
        goForward: (): void => undefined,
        length: 1,
        listen: (): (() => void) => (): void => undefined,
        location: {
          hash: "",
          pathname: "/",
          search: "",
          state: {},
        },
        push: (): void => undefined,
        replace: (): void => undefined,
      },
      location: {
        hash: "",
        pathname: "/",
        search: "",
        state: {},
      },
      match: {
        isExact: true,
        params: {},
        path: "/",
        url: "",
      },
    };
    const renderedComponent: ReactTestRenderer = renderer.create(
      <ThemeProvider theme={theme}>
        <NativeRouter initialEntries={["/"]}>
          <LoginView  {...mockProps} />
        </NativeRouter>
      </ThemeProvider>,
    );
    expect(renderedComponent.toJSON())
      .toBeTruthy();
  });
});
