import { EventContent } from "scenes/Dashboard/containers/EventContent";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import React from "react";
import wait from "waait";
import { MemoryRouter, Route } from "react-router";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";

describe("EventContent", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
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
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventContent).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventContent}
            path={"/:projectName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render header component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/description"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventContent}
            path={"/:projectName/events/:eventId/description"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper.text()).toContain("Solved");
  });
});
