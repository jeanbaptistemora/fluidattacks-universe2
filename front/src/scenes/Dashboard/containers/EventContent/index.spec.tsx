import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { MemoryRouter, RouteComponentProps } from "react-router";
import wait from "waait";
import { EventContent } from "./index";
import { GET_EVENT_HEADER } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("EventContent", () => {
  const mockProps: RouteComponentProps<{ eventId: string }> = {
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
    match: {
      isExact: true,
      params: { eventId: "413372600" },
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [{
    request: {
      query: GET_EVENT_HEADER,
      variables: { eventId: "413372600" },
    },
    result: {
      data: {
        event: {
          eventDate: "2019-12-09 12:00",
          eventStatus: "SOLVED",
          eventType: "OTHER",
          id: "413372600",
        },
      },
    },
  }];

  it("should return a fuction", () => {
    expect(typeof (EventContent))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventContent {...mockProps} />
      </MockedProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render header component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/events/413372600/description"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <EventContent {...mockProps} />
        </MockedProvider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper.text())
      .toContain("Solved");
  });
});
