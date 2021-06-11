import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import wait from "waait";

import { GroupRoute } from "scenes/Dashboard/containers/GroupRoute";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupRoute/queries";

describe("GroupRoute", (): void => {
  const groupMock: Readonly<MockedResponse> = {
    request: {
      query: GET_GROUP_DATA,
      variables: {
        groupName: "TEST",
        organization: "Fluid",
      },
    },
    result: {
      data: {
        alert: {
          message: "Hello world",
          status: 1,
        },
        group: {
          deletionDate: "",
          name: "TEST",
          serviceAttributes: ["has_integrates"],
          userDeletion: "",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupRoute).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const setUserRoleCallback: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider addTypename={false} mocks={[groupMock]}>
        <GroupRoute setUserRole={setUserRoleCallback} />
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(wrapper).toHaveLength(1);
  });
});
