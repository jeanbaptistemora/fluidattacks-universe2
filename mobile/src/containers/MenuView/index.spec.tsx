import React from "react";
import { RouteComponentProps } from "react-router-native";
import renderer, { ReactTestRenderer } from "react-test-renderer";

import { MenuView } from "./index";

describe("MenuView", () => {
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
        pathname: "/Menu",
        search: "",
        state: {
          userInfo: {
            givenName: "Test",
          },
        },
      },
      match: {
        isExact: true,
        params: {},
        path: "/Menu",
        url: "",
      },
    };
    const renderedComponent: ReactTestRenderer = renderer.create(<MenuView {...mockProps} />);
    expect(renderedComponent.toJSON())
      .toBeTruthy();
  });
});
