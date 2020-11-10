import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import _ from "lodash";
import * as React from "react";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { EventContent } from "scenes/Dashboard/containers/EventContent";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";

describe("EventContent", () => {
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
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/description"} component={EventContent}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render header component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/description"} component={EventContent}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper.text())
      .toContain("Solved");
  });
});
