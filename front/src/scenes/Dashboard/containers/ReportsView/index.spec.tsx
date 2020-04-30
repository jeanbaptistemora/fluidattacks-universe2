import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Button } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { ReportsView } from "./index";

describe("ReportsView", () => {

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
      state: {
        userInfo: {
          givenName: "Test",
        },
      },
    },
    match: {
      isExact: true,
      params: {},
      path: "/",
      url: "",
    },
  };

  it("should return a function", () => {
    expect(typeof (ReportsView))
      .toEqual("function");
  });

  it("should render a project box", () => {
    const wrapper: ShallowWrapper = shallow(
      <ReportsView {...mockProps}/>,
    );
    expect(wrapper.find(Button))
      .toBeTruthy();
  });
});
