import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { GET_TOE_LINES } from "./queries";

import { GroupToeLinesView } from ".";
import { DataTableNext } from "components/DataTableNext";
import type { ITableProps } from "components/DataTableNext/types";
import store from "store";

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
            __typename: "Project",
            name: "unittesting",
            roots: [
              {
                __typename: "GitRoot",
                id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                toeLines: [
                  {
                    __typename: "ToeLines",
                    comments: "comment test",
                    filename: "product/test/test.config",
                    loc: 8,
                    modifiedCommit: "983466z",
                    modifiedDate: "2019-08-01T00:00:00-05:00",
                    testedDate: "2021-02-28T00:00:00-05:00",
                    testedLines: 4,
                  },
                ],
              },
              {
                __typename: "GitRoot",
                id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                toeLines: [
                  {
                    __typename: "ToeLines",
                    comments: "comment test",
                    filename: "integrates_1/test2/test.sh",
                    loc: 120,
                    modifiedCommit: "273412t",
                    modifiedDate: "2020-11-19T00:00:00-05:00",
                    testedDate: "2021-01-20T00:00:00-05:00",
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
      <MemoryRouter initialEntries={["/unittesting/toelines"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={[mockedToeLines]}>
            <Route
              component={GroupToeLinesView}
              path={"/:projectName/toelines"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const toeLinesTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblToeLines" });
    const tableHeader: ReactWrapper = toeLinesTable.find("Header");
    const simpleRows: ReactWrapper = toeLinesTable.find("SimpleRow");
    const firstRow: ReactWrapper = simpleRows.at(0);
    const secondRow: ReactWrapper = simpleRows.at(1);

    expect(tableHeader.text()).toStrictEqual(
      [
        "Filename",
        "LOC",
        "Tested lines",
        "Modified date",
        "Modified commit",
        "Tested date",
        "Comments",
      ].join("")
    );
    expect(firstRow.text()).toStrictEqual(
      [
        "integrates_1/test2/test.sh",
        "120",
        "172",
        "2020-11-19",
        "273412t",
        "2021-01-20",
        "comment test",
      ].join("")
    );
    expect(secondRow.text()).toStrictEqual(
      [
        "product/test/test.config",
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
