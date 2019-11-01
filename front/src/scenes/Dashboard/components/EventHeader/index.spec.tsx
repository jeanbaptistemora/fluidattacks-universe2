import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { EventHeader, IEventHeaderProps } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("EventHeader", () => {

  it("should return a function", () => {
    expect(typeof (EventHeader))
      .toEqual("function");
  });

  it("should render event header with evidence", () => {
    const mockProps: IEventHeaderProps  = {
      eventDate: "",
      eventStatus: "",
      eventType: "",
      id: "",
    };
    const wrapper: ShallowWrapper = shallow(
      <EventHeader {...mockProps}/>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render event header without evidence", () => {
    const mockProps: IEventHeaderProps  = {
      eventDate: "",
      eventStatus: "",
      eventType: "",
      id: "",
    };
    const wrapper: ShallowWrapper = shallow(
      <EventHeader {...mockProps}/>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
