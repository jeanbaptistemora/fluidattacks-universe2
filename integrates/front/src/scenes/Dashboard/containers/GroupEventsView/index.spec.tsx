// Needed to allow lazy updates of test components
/* eslint-disable @typescript-eslint/no-unsafe-return */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupEventsView } from "scenes/Dashboard/containers/GroupEventsView";
import { GET_EVENTS } from "scenes/Dashboard/containers/GroupEventsView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            events: [
              {
                accessibility: "Repository",
                affectedComponents: "",
                closingDate: "-",
                detail: "Test description",
                eventDate: "2018-10-17 00:00:00",
                eventStatus: "SOLVED",
                eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                groupName: "unittesting",
                id: "463457733",
              },
            ],
            name: "unittesting",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof GroupEventsView).toStrictEqual("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("Query").children()).toHaveLength(0);
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render events table", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("table")).toHaveLength(1);
    expect(
      wrapper
        .find("td")
        .filterWhere((td: ReactWrapper): boolean =>
          _.includes(td.text(), "Authorization for special attack")
        )
    ).toHaveLength(1);
    expect(
      wrapper
        .find("td")
        .filterWhere((td: ReactWrapper): boolean =>
          td.containsMatchingElement(<span>{"Solved"}</span>)
        )
    ).toHaveLength(1);
  });

  it("should render new event modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_event_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const newButton = (): ReactWrapper =>
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          _.includes(button.text(), "New")
        );

    expect(newButton()).toHaveLength(1);

    newButton().simulate("click");

    const dateField = (): ReactWrapper =>
      wrapper.find({ name: "eventDate" }).find("input");

    const typeField = (): ReactWrapper =>
      wrapper.find({ name: "eventType" }).find("select");

    const contextField = (): ReactWrapper =>
      wrapper.find({ name: "context" }).find("select");

    const checkBoxes = (): ReactWrapper =>
      wrapper
        .find({ name: "accessibility" })
        .find("input")
        .find({ type: "checkbox" });

    const textAreaField = (): ReactWrapper =>
      wrapper.find({ name: "detail" }).find("textarea");

    const actionBeforeBlockingField = (): ReactWrapper =>
      wrapper.find({ name: "actionBeforeBlocking" }).find("select");

    const actionAfterBlockedField = (): ReactWrapper =>
      wrapper.find({ name: "actionAfterBlocking" }).find("select");

    const evidenceFiles = (): ReactWrapper =>
      wrapper.find("span").find(".fa-search");

    expect(wrapper.containsMatchingElement(<h4>{"New Event"}</h4>)).toBe(true);
    expect(dateField()).toHaveLength(1);
    expect(typeField()).toHaveLength(1);
    expect(contextField()).toHaveLength(1);
    expect(checkBoxes()).toHaveLength(2);
    expect(textAreaField()).toHaveLength(1);
    expect(actionBeforeBlockingField()).toHaveLength(1);
    expect(actionAfterBlockedField()).toHaveLength(1);
    expect(evidenceFiles()).toHaveLength(2);
  });
});
