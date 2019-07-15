import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { RouteComponentProps } from "react-router";
import { CommentsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Finding comments view", () => {

  const routePropsMock: RouteComponentProps<{ findingId: string; type: string }> = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: { isExact: true, params: { findingId: "422286126", type: "comments" }, path: "/", url: "" },
  };

  it("should return a function", () => {
    expect(typeof (CommentsView))
      .toEqual("function");
  });

  it("should render a comment view", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView {...routePropsMock} />,
    );
    expect(wrapper.html())
      .toEqual('<div id="finding-comments"></div>');
  });

  it("should render an observation view", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView
        {...routePropsMock}
        match={{ ...routePropsMock.match, params: { findingId: "422286126", type: "observations" } }}
      />,
    );
    expect(wrapper.html())
      .toEqual('<div id="finding-observations"></div>');
  });
});
