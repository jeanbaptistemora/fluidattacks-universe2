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
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            toeInputs: [
              {
                component: "test.com/api/Test",
                createdDate: "2000-01-01T00:00:00-05:00",
                entryPoint: "idTest",
                seenFirstTimeBy: "",
                testedDate: "2020-01-02T00:00:00-05:00",
                unreliableRootNickname: "test_nickname",
              },
              {
                component: "test.com/test/test.aspx",
                createdDate: "2020-03-14T00:00:00-05:00",
                entryPoint: "btnTest",
                seenFirstTimeBy: "test@test.com",
                testedDate: "2021-02-02T00:00:00-05:00",
                unreliableRootNickname: "test_nickname",
              },
              {
                component: "test.com/test2/test.aspx",
                createdDate: "2020-01-11T00:00:00-05:00",
                entryPoint: "-",
                seenFirstTimeBy: "test2@test.com",
                testedDate: "2021-02-11T00:00:00-05:00",
                unreliableRootNickname: "",
              },
            ],
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
        "Root",
        "Entry point",
        "Attacked at",
        "Seen at",
        "Seen first time by",
      ].join("")
    );
    expect(firstRow.text()).toStrictEqual(
      ["test_nickname", "idTest", "2020-01-02", "2000-01-01", ""].join("")
    );
    expect(secondRow.text()).toStrictEqual(
      [
        "test_nickname",
        "btnTest",
        "2021-02-02",
        "2020-03-14",
        "test@test.com",
      ].join("")
    );
    expect(thirdRow.text()).toStrictEqual(
      ["", "-", "2021-02-11", "2020-01-11", "test2@test.com"].join("")
    );
  });
});
