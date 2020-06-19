import { SubscriptionResult } from "@apollo/react-common";
import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router";
import store from "../../store/index";
import { Dashboard } from "./index";
import { GET_USER_PERMISSIONS } from "./queries";
import { IGetUserPermissionsAttr } from "./types";

describe("Dashboard", () => {
  it("should return a function", () => {
    expect(typeof (Dashboard))
      .toEqual("function");
  });

  it("should render dashboard component", async (): Promise<void> => {
    const permissionsResult: IGetUserPermissionsAttr = {
      me: {
        permissions: ["dummyPermission", "dummyPermissionBrother"],
      },
    };

    const subscriptionResult: SubscriptionResult = {
      data: {
        broadcast: "broadcastTestResult",
      },
      error: undefined,
      loading: true,
    };

    const mocks: ReadonlyArray<MockedResponse> = [
      {
        request: {
          query: GET_USER_PERMISSIONS,
          variables: {
            projectName: "TEST",
          },
        },
        result: {
          data: permissionsResult,
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/integrates"]}>
        <MockedProvider mocks={mocks}>
          <Provider store={store}>
            <Dashboard />
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );

    await act(async () => { await wait(0); wrapper.update(); });

    const sideBar: ReactWrapper = wrapper.find("sidebar");

    const scrollUpButton: ReactWrapper = wrapper.find("scrollUpButton");

    const navBar: ReactWrapper = wrapper
      .find({ id: "navbar" })
      .find("Row");

    expect(wrapper)
      .toHaveLength(1);
    expect(sideBar)
      .toHaveLength(1);
    expect(scrollUpButton)
      .toHaveLength(1);
    expect(navBar)
      .toHaveLength(1);
  });
});
