import React from "react";
import { RouteComponentProps } from "react-router-native";
import renderer, { ReactTestRenderer } from "react-test-renderer";

import { LoginView } from "./index";

describe("LoginView", () => {
  it("should render", () => {

    const mockProps: RouteComponentProps = {
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
    const renderedComponent: ReactTestRenderer = renderer.create(<LoginView {...mockProps} />);
    expect(renderedComponent.toJSON())
      .toBeTruthy();
  });
});
