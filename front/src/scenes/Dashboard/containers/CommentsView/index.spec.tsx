import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider } from "react-apollo/test-utils";
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
      <MockedProvider mocks={[]} addTypename={true}>
        <CommentsView {...routePropsMock} />
      </MockedProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an observation view", () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[]} addTypename={true}>
        <CommentsView
          {...routePropsMock}
          match={{ ...routePropsMock.match, params: { findingId: "422286126", type: "observations" } }}
        />
      </MockedProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
