import { GET_USER_AUTHORIZATION } from "scenes/Registration/containers/WelcomeView/queries";
import { MemoryRouter } from "react-router-dom";
import { Provider } from "react-redux";
import React from "react";
import { WelcomeView } from "scenes/Registration/containers/WelcomeView";
import _ from "lodash";
import { act } from "react-dom/test-utils";
import store from "store";
import { translate } from "utils/translations/translate";
import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { ReactWrapper, mount } from "enzyme";

describe("Welcome view", (): void => {
  // Necessary to setup the window object within the test.
  // eslint-disable-next-line fp/no-mutation
  (window as typeof window & { userName: string }).userName = "Test";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof WelcomeView).toStrictEqual("function");
  });

  it("should render greetings message", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <WelcomeView />
      </MockedProvider>
    );

    expect(wrapper.text()).toContain("Hello Test!");
  });

  it("should render legal notice", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: { query: GET_USER_AUTHORIZATION },
        result: {
          data: { me: { remember: false } },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <WelcomeView />
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    expect(wrapper.find("modal").text()).toContain(
      "Integrates, Copyright (c) 2020 Fluid Attacks"
    );
  });

  it("should render already logged in", (): void => {
    expect.hasAssertions();

    localStorage.setItem("showAlreadyLoggedin", "1");
    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <WelcomeView />
      </MockedProvider>
    );

    expect(wrapper.find("h3").text()).toContain("You are already logged in");
  });

  it("should render concurrent session", (): void => {
    expect.hasAssertions();

    localStorage.setItem("showAlreadyLoggedin", "0");
    localStorage.setItem("concurrentSession", "1");
    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <WelcomeView />
      </MockedProvider>
    );

    expect(wrapper.find("h3").text()).toContain(
      translate.t("registration.concurrent_session_message")
    );
  });

  it("should clear localstorage before redirect", (): void => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: { query: GET_USER_AUTHORIZATION },
        result: {
          data: { me: { remember: false } },
        },
      },
    ];
    localStorage.setItem("showAlreadyLoggedin", "1");
    localStorage.setItem(
      "start_url",
      "/project/BWAPP/vulns/413372600/consulting"
    );
    const wrapper: ReactWrapper = mount(
      <MemoryRouter>
        <MockedProvider addTypename={false} mocks={mocks}>
          <WelcomeView />
        </MockedProvider>
      </MemoryRouter>
    );

    wrapper.find("Button").simulate("click");

    expect(_.get(localStorage, "showAlreadyLoggedin")).toBeUndefined();
    expect(_.get(localStorage, "start_url")).toBeUndefined();
  });
});
