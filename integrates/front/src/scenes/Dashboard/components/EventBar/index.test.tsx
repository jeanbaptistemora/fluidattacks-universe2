/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_ORG_EVENTS } from "./queries";

import { EventBar } from "scenes/Dashboard/components/EventBar";

describe("EventBar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof EventBar).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    const organizationName: string = "testOrgName";
    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORG_EVENTS,
          variables: {
            organizationName,
          },
        },
        result: {
          data: {
            organizationId: {
              groups: [
                {
                  events: [
                    {
                      eventDate: "2022-04-02 03:02:00",
                      eventStatus: "CREATED",
                      groupName: "group1",
                    },
                    {
                      eventDate: "2022-05-01 06:18:00",
                      eventStatus: "CREATED",
                      groupName: "group1",
                    },
                  ],
                  name: "group1",
                },
                {
                  events: [
                    {
                      eventDate: "2022-02-01 09:30:00",
                      eventStatus: "SOLVED",
                      groupName: "group2",
                    },
                  ],
                  name: "group2",
                },
              ],
              name: organizationName,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter>
        <MockedProvider addTypename={false} mocks={mocks}>
          <EventBar organizationName={organizationName} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.events.eventBar.message")
      ).toBeInTheDocument();
    });

    expect(screen.queryByRole("link")).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute(
      "href",
      `/orgs/${organizationName}/groups`
    );

    await userEvent.hover(screen.getByText("group.events.eventBar.message"));

    expect(
      screen.queryByText("group.events.eventBar.tooltip")
    ).toBeInTheDocument();
  });
});
