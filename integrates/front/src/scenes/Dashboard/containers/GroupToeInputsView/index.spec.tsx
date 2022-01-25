import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GET_TOE_INPUTS } from "./queries";

import { GroupToeInputsView } from ".";
import { DataTableNext } from "components/DataTableNext";
import type { ITableProps } from "components/DataTableNext/types";
import { authzPermissionsContext } from "utils/authz/config";

describe("GroupToeInputsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeInputsView).toStrictEqual("function");
  });

  it("should display group toe inputs", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeInputs: MockedResponse = {
      request: {
        query: GET_TOE_INPUTS,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetBePresentUntil: true,
          canGetFirstAttackAt: true,
          canGetSeenFirstTimeBy: true,
          first: 300,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            toeInputs: {
              __typename: "ToeInputsConnection",
              edges: [
                {
                  node: {
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    bePresent: true,
                    component: "test.com/api/Test",
                    entryPoint: "idTest",
                    hasVulnerabilities: false,
                    seenAt: "2000-01-01T05:00:00+00:00",
                    seenFirstTimeBy: "",
                    unreliableRootNickname: "test_nickname",
                  },
                },
                {
                  node: {
                    attackedAt: "2021-02-02T00:00:00-05:00",
                    bePresent: true,
                    component: "test.com/test/test.aspx",
                    entryPoint: "btnTest",
                    hasVulnerabilities: true,
                    seenAt: "2020-03-14T00:00:00-05:00",
                    seenFirstTimeBy: "test@test.com",
                    unreliableRootNickname: "test_nickname",
                  },
                },
                {
                  node: {
                    attackedAt: "2021-02-11T00:00:00-05:00",
                    bePresent: false,
                    component: "test.com/test2/test.aspx",
                    entryPoint: "-",
                    hasVulnerabilities: true,
                    seenAt: "2020-01-11T00:00:00-05:00",
                    seenFirstTimeBy: "test2@test.com",
                    unreliableRootNickname: "",
                  },
                },
              ],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
            },
          },
        },
      },
    };
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_toe_input_attacked_at_resolve" },
      { action: "api_resolvers_toe_input_attacked_by_resolve" },
      { action: "api_resolvers_toe_input_be_present_until_resolve" },
      { action: "api_resolvers_toe_input_first_attack_at_resolve" },
      { action: "api_resolvers_toe_input_seen_first_time_by_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/surface/inputs"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeInputs]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/inputs"}>
              <GroupToeInputsView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const toeInputsTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblToeInputs" });
    const tableHeader: ReactWrapper = toeInputsTable.find("Header");
    const simpleRows: ReactWrapper = toeInputsTable.find("SimpleRow");
    const firstRow: ReactWrapper = simpleRows.at(0);
    const secondRow: ReactWrapper = simpleRows.at(1);
    const thirdRow: ReactWrapper = simpleRows.at(2);

    expect(tableHeader.text()).toStrictEqual(
      [
        "Root",
        "Entry point",
        "Has vulnerabilities",
        "Attacked at",
        "Seen at",
        "Seen first time by",
      ].join("")
    );
    expect(firstRow.text()).toStrictEqual(
      ["test_nickname", "idTest", "No", "2020-01-02", "2000-01-01", ""].join("")
    );
    expect(secondRow.text()).toStrictEqual(
      [
        "test_nickname",
        "btnTest",
        "Yes",
        "2021-02-02",
        "2020-03-14",
        "test@test.com",
      ].join("")
    );
    expect(thirdRow.text()).toStrictEqual(
      ["", "-", "Yes", "2021-02-11", "2020-01-11", "test2@test.com"].join("")
    );
  });
});
