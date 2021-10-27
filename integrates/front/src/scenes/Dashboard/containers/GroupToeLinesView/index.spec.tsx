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
            roots: [
              {
                __typename: "GitRoot",
                id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                nickname: "product",
                servicesToeLines: [
                  {
                    __typename: "ServicesToeLines",
                    comments: "comment test",
                    filename: "product/test/test.config",
                    loc: 8,
                    modifiedCommit: "983466z",
                    modifiedDate: "2019-08-01T05:00:00+00:00",
                    sortsRiskLevel: 0,
                    testedDate: "2021-02-28T05:00:00+00:00",
                    testedLines: 4,
                  },
                ],
              },
              {
                __typename: "GitRoot",
                id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                nickname: "asm_1",
                servicesToeLines: [
                  {
                    __typename: "ServicesToeLines",
                    comments: "comment test",
                    filename: "asm_1/test2/test.sh",
                    loc: 172,
                    modifiedCommit: "273412t",
                    modifiedDate: "2020-11-19T05:00:00+00:00",
                    sortsRiskLevel: 0,
                    testedDate: "2021-01-20T05:00:00+00:00",
                    testedLines: 172,
                  },
                ],
              },
            ],
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
        "asm_1",
        "100%",
        "172",
        "172",
        "2020-11-19",
        "273412t",
        "2021-01-20",
        "comment test",
      ].join("")
    );
    expect(secondRow.text()).toStrictEqual(
      [
        "product",
        "50%",
        "8",
        "4",
        "2019-08-01",
        "983466z",
        "2021-02-28",
        "comment test",
      ].join("")
    );
  });
});
