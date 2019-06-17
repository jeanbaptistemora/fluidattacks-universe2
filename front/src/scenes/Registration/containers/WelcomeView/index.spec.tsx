import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { component as WelcomeView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Welcome view", () => {
  it("should return a function", () => {
    expect(typeof (WelcomeView)).to
      .equal("function");
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

    expect(wrapper).to.have
      .length(1);
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

    expect(wrapper.contains(<h1>registration.greeting Test!</h1>)).to
      .equal(true);
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

    expect(wrapper.contains(<p>registration.unauthorized</p>)).to
      .equal(true);
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

    expect(wrapper.find({ id: "legalNotice" }).length).to
      .equal(1);
  });
});
