import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import _ from "lodash";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import { WelcomeView } from "./index";
import { GET_USER_AUTHORIZATION } from "./queries";

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

  it("should render unauthorized message", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: { query: GET_USER_AUTHORIZATION },
      result: {
        data: { me: { authorized: false, remember: false } },
      },
    }];
    const locationMock: jest.Mock = jest.fn();
    window.location.assign = locationMock;

    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <WelcomeView {...routeProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("You do not have authorization for login yet");
    wrapper.find("Button")
      .filterWhere((btn: ReactWrapper) => btn.contains("Log out"))
      .simulate("click");
    expect(locationMock)
      .toHaveBeenCalledWith("/integrates/logout");
  });

  it("should render legal notice", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: { query: GET_USER_AUTHORIZATION },
      result: {
        data: { me: { authorized: true, remember: false } },
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
      .toContain("Integrates, Copyright (c) 2019 Fluid Attacks");
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

  it("should clear localstorage on unmount", () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: { query: GET_USER_AUTHORIZATION },
      result: {
        data: { me: { authorized: false, remember: false } },
      },
    }];
    localStorage.setItem("showAlreadyLoggedin", "1");
    localStorage.setItem("url_inicio", "!/project/BWAPP/findings/413372600/comments");
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <WelcomeView {...routeProps} />
      </MockedProvider>,
    );
    wrapper.unmount();
    expect(_.get(localStorage, "showAlreadyLoggedin"))
      .toEqual(undefined);
    expect(_.get(localStorage, "url_inicio"))
      .toEqual(undefined);
  });
});
