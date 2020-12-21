import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { RecordsView } from "scenes/Dashboard/containers/RecordsView";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/RecordsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingRecordsView", () => {
  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_FINDING_RECORDS,
      variables: { findingId: "422286126" },
    },
    result: {
      data: {
        finding: {
          id: "422286126",
          records: JSON.stringify([
            { Character: "Cobra Commander", Genre: "action", Release: "2013", Title: "G.I. Joe: Retaliation" },
            { Character: "Tony Stark", Genre: "action", Release: "2008", Title: "Iron Man" },
          ]),
        },
      },
    },
  }];

  it("should return a function", (): void => {
    expect(typeof (RecordsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route component={RecordsView} path={"/:projectName/vulns/:findingId/records"}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const table: ReactWrapper = wrapper.find("BootstrapTable");
    expect(table)
      .toHaveLength(1);
    expect(table.find("HeaderCell"))
      .toHaveLength(4);
  });

  it("should render as editable", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_update_evidence_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route component={RecordsView} path={"/:projectName/vulns/:findingId/records"}/>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    expect(editButton)
      .toHaveLength(1);
    editButton.simulate("click");
    expect(wrapper.contains("Update"))
      .toBe(true);
  });

  it("should render as readonly", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route component={RecordsView} path={"/:projectName/vulns/:findingId/records"}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.contains("Edit"))
      .toBe(false);
  });

  it("should render delete button", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_update_evidence_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route component={RecordsView} path={"/:projectName/vulns/:findingId/records"}/>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const editButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Edit"))
      .at(0);
    expect(editButton)
      .toHaveLength(1);
    editButton.simulate("click");
    expect(wrapper.contains("Delete"))
      .toBe(true);
  });

  it("should render empty UI", async () => {
    const emptyMocks: ReadonlyArray<MockedResponse> = [{
      request: {
        query: GET_FINDING_RECORDS,
        variables: { findingId: "422286126" },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            records: "[]",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider mocks={emptyMocks} addTypename={false}>
          <Route component={RecordsView} path={"/:projectName/vulns/:findingId/records"}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("There are no records");
  });
});
