import { render, screen } from "@testing-library/react";
import React from "react";

import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import type { IEventHeaderProps } from "scenes/Dashboard/components/EventHeader";

describe("EventHeader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EventHeader).toBe("function");
  });

  it("should render event header with evidence", (): void => {
    expect.hasAssertions();

    const mockProps: IEventHeaderProps = {
      eventDate: "",
      eventStatus: "SOLVED",
      eventType: "",
      id: "",
    };
    render(
      <EventHeader
        eventDate={mockProps.eventDate}
        eventStatus={mockProps.eventStatus}
        eventType={mockProps.eventType}
        id={mockProps.id}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabEvents.id")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabEvents.statusValues.solve")
    ).toBeInTheDocument();
  });

  it("should render event header without evidence", (): void => {
    expect.hasAssertions();

    const mockProps: IEventHeaderProps = {
      eventDate: "2019-04-02 03:02:00",
      eventStatus: "CREATED",
      eventType: "",
      id: "540462628",
    };
    render(
      <EventHeader
        eventDate={mockProps.eventDate}
        eventStatus={mockProps.eventStatus}
        eventType={mockProps.eventType}
        id={mockProps.id}
      />
    );

    expect(
      screen.queryByText("searchFindings.tabEvents.id")
    ).toBeInTheDocument();
    expect(screen.queryByText("540462628")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabEvents.statusValues.unsolve")
    ).toBeInTheDocument();
    expect(screen.queryByText("2019-04-02 03:02:00")).toBeInTheDocument();
  });
});
