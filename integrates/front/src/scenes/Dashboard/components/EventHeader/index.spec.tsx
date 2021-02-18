import { EventHeader } from "scenes/Dashboard/components/EventHeader";
import type { IEventHeaderProps } from "scenes/Dashboard/components/EventHeader";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("EventHeader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof EventHeader).toStrictEqual("function");
  });

  it("should render event header with evidence", (): void => {
    expect.hasAssertions();

    const mockProps: IEventHeaderProps = {
      eventDate: "",
      eventStatus: "",
      eventType: "",
      id: "",
    };
    const wrapper: ShallowWrapper = shallow(
      <EventHeader
        eventDate={mockProps.eventDate}
        eventStatus={mockProps.eventStatus}
        eventType={mockProps.eventType}
        id={mockProps.id}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render event header without evidence", (): void => {
    expect.hasAssertions();

    const mockProps: IEventHeaderProps = {
      eventDate: "",
      eventStatus: "",
      eventType: "",
      id: "",
    };
    const wrapper: ShallowWrapper = shallow(
      <EventHeader
        eventDate={mockProps.eventDate}
        eventStatus={mockProps.eventStatus}
        eventType={mockProps.eventType}
        id={mockProps.id}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
