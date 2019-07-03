import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { component as WelcomeView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Welcome view", () => {
  it("should return a function", () => {
    expect(typeof (WelcomeView))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        legalNotice={{ open: true, rememberDecision: false }}
        username={"Test"}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render greetings message", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        legalNotice={{ open: true, rememberDecision: false }}
        username={"Test"}
      />,
    );
    expect(wrapper.contains("Hello"))
      .toEqual(true);
  });

  it("should render unauthorized message", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={false}
        isRememberEnabled={false}
        legalNotice={{ open: true, rememberDecision: false }}
        username={"Test"}
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

  it("should render legal notice", () => {
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView
        email={"unittesting@fluidattacks.com"}
        isAuthorized={true}
        isRememberEnabled={false}
        legalNotice={{ open: true, rememberDecision: false }}
        username={"Test"}
      />,
    );

    expect(wrapper.find({ id: "legalNotice" }).length)
      .toEqual(1);
  });
});
