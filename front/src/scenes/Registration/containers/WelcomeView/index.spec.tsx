import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { RouteComponentProps } from "react-router-dom";
import { WelcomeView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Welcome view", () => {

  const routeProps: RouteComponentProps = {
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
    match: { isExact: true, params: {}, path: "/", url: "" },
  };

  it("should return a function", () => {
    expect(typeof (WelcomeView))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        {...routeProps}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render greetings message", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        {...routeProps}
      />,
    );
    expect(wrapper.contains("Hello"))
      .toEqual(true);
  });

  it.skip("should render unauthorized message", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        {...routeProps}
      />,
    );

    expect(wrapper.contains(
      <p>
        You do not have authorization for login yet. Please contact Fluid Attacks&#39;s staff or
        your project administrator to get access.
      </p>,
    ))
      .toEqual(true);
  });

  it.skip("should render legal notice", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        {...routeProps}
      />,
    );

    expect(wrapper.find({ id: "legalNotice" }).length)
      .toEqual(1);
  });
});
