import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import store from "../../../../store";
import { RecordsView } from "./index";
import { GET_FINDING_RECORDS } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("FindingRecordsView", () => {

  const routePropsMock: RouteComponentProps<{ findingId: string }> = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: { isExact: true, params: { findingId: "422286126" }, path: "/", url: "" },
  };

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
      <MockedProvider mocks={mocks} addTypename={false}>
        <RecordsView {...routePropsMock} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const table: ReactWrapper = wrapper.find("BootstrapTable");
    expect(table)
      .toHaveLength(1);
    expect(table.find("HeaderCell"))
      .toHaveLength(4);
  });

  it("should render as editable", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <RecordsView {...routePropsMock} />
        </MockedProvider>
      </Provider>,
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
    (window as typeof window & { userRole: string }).userRole = "customer";
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <RecordsView {...routePropsMock} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.contains("Edit"))
      .toBe(false);
  });

  it("should render delete button", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <RecordsView {...routePropsMock} />
        </MockedProvider>
      </Provider>,
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
      <MockedProvider mocks={emptyMocks} addTypename={false}>
        <RecordsView {...routePropsMock} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("There are no records");
  });
});
