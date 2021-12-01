import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GET_TOE_LINES } from "./queries";

import { GroupToeLinesView } from ".";
import { DataTableNext } from "components/DataTableNext";
import type { ITableProps } from "components/DataTableNext/types";

describe("GroupToeLinesView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeLinesView).toStrictEqual("function");
  });

  it("should display group toe lines", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            toeLines: {
              __typename: "ToeLinesConnection",
              edges: [
                {
                  node: {
                    attackedAt: "2021-02-20T05:00:00+00:00",
                    attackedBy: "test2@test.com",
                    attackedLines: 4,
                    bePresent: true,
                    bePresentUntil: "",
                    comments: "comment 1",
                    commitAuthor: "customer@gmail.com",
                    filename: "test/test#.config",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    loc: 8,
                    modifiedCommit: "983466z",
                    modifiedDate: "2020-11-15T15:41:04+00:00",
                    root: {
                      nickname: "product",
                    },
                    seenAt: "2020-02-01T15:41:04+00:00",
                    sortsRiskLevel: 80,
                  },
                },
                {
                  node: {
                    attackedAt: "",
                    attackedBy: "test@test.com",
                    attackedLines: 120,
                    bePresent: false,
                    bePresentUntil: "2021-01-01T15:41:04+00:00",
                    comments: "comment 2",
                    commitAuthor: "customer@gmail.com",
                    filename: "test2/test.sh",
                    firstAttackAt: "",
                    loc: 172,
                    modifiedCommit: "273412t",
                    modifiedDate: "2020-11-16T15:41:04+00:00",
                    root: {
                      nickname: "integrates_1",
                    },
                    seenAt: "2020-01-01T15:41:04+00:00",
                    sortsRiskLevel: 0,
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
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeLines]}>
          <Route
            component={GroupToeLinesView}
            path={"/:groupName/surface/lines"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const toeLinesTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblToeLines" });
    const tableHeader: ReactWrapper = toeLinesTable.find("Header");
    const simpleRows: ReactWrapper = toeLinesTable.find("SimpleRow");
    const firstRow: ReactWrapper = simpleRows.at(0);
    const secondRow: ReactWrapper = simpleRows.at(1);

    expect(tableHeader.text()).toStrictEqual(
      [
        "Be present",
        "Root",
        "Coverage",
        "LOC",
        "Attacked lines",
        "Modified date",
        "Modified commit",
        "Attacked at",
        "Comments",
      ].join("")
    );
    expect(firstRow.text()).toStrictEqual(
      [
        "Yes",
        "product",
        "50%",
        "8",
        "4",
        "2020-11-15",
        "983466z",
        "2021-02-20",
        "comment 1",
      ].join("")
    );

    expect(secondRow.text()).toStrictEqual(
      [
        "No",
        "integrates_1",
        "70%",
        "172",
        "120",
        "2020-11-16",
        "273412t",
        "",
        "comment 2",
      ].join("")
    );
  });
});
