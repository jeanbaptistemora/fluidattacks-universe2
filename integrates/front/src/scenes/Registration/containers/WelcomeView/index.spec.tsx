import { GET_USER_AUTHORIZATION } from "scenes/Registration/containers/WelcomeView/queries";
import { MemoryRouter } from "react-router-dom";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { WelcomeView } from "scenes/Registration/containers/WelcomeView";
import _ from "lodash";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";
import store from "store";
import { translate } from "utils/translations/translate";
import { MockedProvider, wait } from "@apollo/react-testing";

describe("Welcome view", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof WelcomeView).toStrictEqual("function");
  });

  it("should render greetings message", async (): Promise<void> => {
    expect.hasAssertions();

    const mock: MockedResponse = {
      request: { query: GET_USER_AUTHORIZATION },
      result: { data: { me: { remember: false, userName: "Test" } } },
    };
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={[mock]}>
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

    expect(wrapper.text()).toContain("Hello Test!");
  });

  it("should render legal notice", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: { query: GET_USER_AUTHORIZATION },
        result: {
          data: { me: { remember: false, userName: "Test" } },
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

  it("should render concurrent session", (): void => {
    expect.hasAssertions();

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

    expect(_.get(localStorage, "start_url")).toBeUndefined();
  });
});
