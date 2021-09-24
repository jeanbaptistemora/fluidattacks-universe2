import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";

import { Sidebar } from "./components/Sidebar";

import { Dashboard } from "scenes/Dashboard";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { GET_USER } from "scenes/Dashboard/queries";
import type { IUser } from "scenes/Dashboard/types";

describe("Dashboard", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dashboard).toStrictEqual("function");
  });

  it("should render dashboard component", async (): Promise<void> => {
    expect.hasAssertions();

    const permissionsResult: IUser = {
      me: {
        isConcurrentSession: false,
        permissions: ["dummyPermission", "dummyPermissionBrother"],
        remember: false,
        sessionExpiration: "2021-01-20 21:37:37.944176",
        userEmail: "",
        userName: "",
      },
    };
    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_USER,
          variables: {
            groupName: "TEST",
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
                  name: "okada",
                },
              ],
              userEmail: "test@fluidattacks.com",
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
                  name: "okada",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider mocks={mocks}>
          <Dashboard />
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const sideBar = wrapper.find(Sidebar);
    const scrollUpButton: ReactWrapper = wrapper.find("ScrollUp");
    const navBar: ReactWrapper = wrapper.find({ id: "navbar" });

    expect(wrapper).toHaveLength(1);
    expect(sideBar).toHaveLength(1);
    expect(scrollUpButton).toHaveLength(1);
    expect(navBar.length).toBeGreaterThan(0);
  });
});
