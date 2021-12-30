import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
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
        variables: { first: 300, groupName: "unittesting" },
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/surface/inputs"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeInputs]}>
          <Route
            component={GroupToeInputsView}
            path={"/:groupName/surface/inputs"}
          />
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
        "Be present",
        "Root",
        "Entry point",
        "Attacked at",
        "Seen at",
        "Seen first time by",
      ].join("")
    );
    expect(firstRow.text()).toStrictEqual(
      ["Yes", "test_nickname", "idTest", "2020-01-02", "2000-01-01", ""].join(
        ""
      )
    );
    expect(secondRow.text()).toStrictEqual(
      [
        "Yes",
        "test_nickname",
        "btnTest",
        "2021-02-02",
        "2020-03-14",
        "test@test.com",
      ].join("")
    );
    expect(thirdRow.text()).toStrictEqual(
      ["No", "", "-", "2021-02-11", "2020-01-11", "test2@test.com"].join("")
    );
  });
});
