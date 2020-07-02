import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { ProjectRoute } from "./index";
import { GET_GROUP_DATA } from "./queries";

describe("ProjectRoute", () => {

  const groupMock: Readonly<MockedResponse> = {
    request: {
      query: GET_GROUP_DATA,
      variables: {
        organization: "Fluid",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        alert: {
          message: "Hello world",
          status: 1,
        },
        project: {
          deletionDate: "",
          serviceAttributes: ["has_integrates"],
          userDeletion: "",
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (ProjectRoute))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const setUserRoleCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[groupMock]} addTypename={false}>
        <ProjectRoute setUserRole={setUserRoleCallback}/>
      </MockedProvider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render alert", async () => {
    const setUserRoleCallback: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility();
    (window as typeof window & Dictionary<string>).userEmail = "test";
    (window as typeof window & Dictionary<string>).userOrganization = "Fluid";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <MockedProvider mocks={[groupMock]} addTypename={false}>
          <Route path="/project/:projectName">
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <ProjectRoute setUserRole={setUserRoleCallback}/>
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Hello world");
  });
});
