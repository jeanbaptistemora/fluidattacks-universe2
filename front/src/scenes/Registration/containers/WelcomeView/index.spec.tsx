import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import _ from "lodash";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import translate from "../../../../utils/translations/translate";
import { WelcomeView } from "./index";
import { GET_USER_AUTHORIZATION } from "./queries";

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
      <WelcomeView {...routeProps} />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render greetings message", () => {
    (window as typeof window & { userName: string }).userName = "Test";
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView {...routeProps} />,
    );
    expect(wrapper.text())
      .toContain("Hello Test!");
  });

  it("should render legal notice", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: { query: GET_USER_AUTHORIZATION },
      result: {
        data: { me: { remember: false } },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <WelcomeView {...routeProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("modal")
      .text())
      .toContain("Integrates, Copyright (c) 2020 Fluid Attacks");
  });

  it("should render already logged in", () => {
    localStorage.setItem("showAlreadyLoggedin", "1");
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView {...routeProps} />,
    );
    expect(wrapper.find("h3")
      .text())
      .toContain("You are already logged in");
  });

  it("should render concurrent session", () => {
    localStorage.setItem("showAlreadyLoggedin", "0");
    localStorage.setItem("concurrentSession", "1");
    const wrapper: ShallowWrapper = shallow(
      <WelcomeView {...routeProps} />,
    );
    expect(wrapper.find("h3")
      .text())
      .toContain(translate.t("registration.concurrent_session_message"));
  });

  it("should clear localstorage before redirect", () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: { query: GET_USER_AUTHORIZATION },
      result: {
        data: { me: { remember: false } },
      },
    }];
    localStorage.setItem("showAlreadyLoggedin", "1");
    localStorage.setItem("start_url", "/project/BWAPP/vulns/413372600/consulting");
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <WelcomeView {...routeProps} />
      </MockedProvider>,
    );

    wrapper.find("Button")
      .simulate("click");
    expect(_.get(localStorage, "showAlreadyLoggedin"))
      .toEqual(undefined);
    expect(_.get(localStorage, "start_url"))
      .toEqual(undefined);
  });
});
