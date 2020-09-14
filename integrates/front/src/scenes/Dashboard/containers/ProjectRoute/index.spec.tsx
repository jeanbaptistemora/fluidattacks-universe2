import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";

import { ProjectRoute } from "scenes/Dashboard/containers/ProjectRoute";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectRoute/queries";

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
});
