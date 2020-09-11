import { Dashboard } from "scenes/Dashboard";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { GET_USER_PERMISSIONS } from "scenes/Dashboard/queries";
import { IGetUserPermissionsAttr } from "scenes/Dashboard/types";
import { MemoryRouter } from "react-router";
import { Provider } from "react-redux";
import React from "react";
import { act } from "react-dom/test-utils";
import store from "store";
import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { ReactWrapper, mount } from "enzyme";

describe("Dashboard", (): void => {
  // Necessary to setup the window object within the test.
  // eslint-disable-next-line fp/no-mutation
  (window as typeof window & { userEmail: string }).userEmail = "test@test.com";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dashboard).toStrictEqual("function");
  });

  it("should render dashboard component", async (): Promise<void> => {
    expect.hasAssertions();

    const permissionsResult: IGetUserPermissionsAttr = {
      me: {
        permissions: ["dummyPermission", "dummyPermissionBrother"],
      },
    };
    const mocks: readonly MockedResponse[] = [
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
      {
        request: {
          query: GET_USER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  name: "imamura",
                },
              ],
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_ORGANIZATIONS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: [
                {
                  __typename: "Organization",
                  name: "imamura",
                },
              ],
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/imamura"]}>
        <MockedProvider mocks={mocks}>
          <Provider store={store}>
            <Dashboard />
          </Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const sideBar: ReactWrapper = wrapper.find("sidebar");
    const scrollUpButton: ReactWrapper = wrapper.find("ScrollUp");
    const navBar: ReactWrapper = wrapper.find({ id: "navbar" });

    expect(wrapper).toHaveLength(1);
    expect(sideBar).toHaveLength(1);
    expect(scrollUpButton).toHaveLength(1);
    expect(navBar.length).toBeGreaterThan(0);
  });
});
