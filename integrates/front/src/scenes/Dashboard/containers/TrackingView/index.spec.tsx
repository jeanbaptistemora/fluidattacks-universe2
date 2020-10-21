import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { RouteComponentProps } from "react-router";
import wait from "waait";

import { TrackingView } from "scenes/Dashboard/containers/TrackingView";
import { GET_FINDING_TRACKING } from "scenes/Dashboard/containers/TrackingView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingExploitView", (): void => {

  const mockProps: RouteComponentProps<{ findingId: string }> = {
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
      query: GET_FINDING_TRACKING,
      variables: { findingId: "422286126" },
    },
    result: {
      data: {
        finding: {
          id: "422286126",
          tracking: [
            { closed: 0, cycle: 0, date: "2018-09-28", effectiveness: 0, open: 1 },
            { closed: 1, cycle: 1, date: "2019-01-08", effectiveness: 100, open: 0 },
          ],
        },
      },
    },
  }];

  it("should return a function", (): void => {
    expect(typeof (TrackingView))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingView {...mockProps} />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render timeline", async () => {
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <TrackingView {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.find("ul"))
      .toHaveLength(1);
    expect(wrapper.find("li"))
      .toHaveLength(2);
  });

  it("should render pending vulns", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_new_finding_pending_vulns_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <TrackingView {...mockProps} />
        </authzPermissionsContext.Provider>
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Pending");
  });
});
