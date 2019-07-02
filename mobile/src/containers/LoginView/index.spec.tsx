import React from "react";
import renderer, { ReactTestRenderer } from "react-test-renderer";

import { ILoginProps, loginView as LoginView } from "./index";
import { initialState } from "./reducer";

jest.mock("Platform", () => {
  const platform: { OS: string } = (jest.requireActual("Platform") as { OS: string });
  platform.OS = "test-env";

  return platform;
});

describe("LoginView", () => {
  it("should render", () => {

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
      ...initialState,
      onGoogleLogin: (): void => undefined,
      onResolveVersion: (): void => undefined,
    };
    const renderedComponent: ReactTestRenderer = renderer.create(<LoginView {...mockProps} />);
    expect(renderedComponent.toJSON())
      .toBeTruthy();
  });
});
