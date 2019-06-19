import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { EventHeader, IEventHeaderProps } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => JSX.Element) = (): JSX.Element => <div />;

describe("EventHeader", () => {

  it("should return a function", () => {
    expect(typeof (EventHeader))
      .toEqual("function");
  });

  it("should render", () => {
    const mockProps: IEventHeaderProps  = {
      eventData: {
        accessibility: "",
        affectation: "",
        affectedComponents: "",
        analyst: "",
        client: "",
        clientProject: "",
        detail: "",
        eventDate: "",
        eventStatus: "",
        eventType: "",
        evidence: "",
        id: "",
        projectName: "",
      },
      isActiveTab: true,
      urlDescription: functionMock,
      urlEvidence: functionMock,
    };
    const wrapper: ShallowWrapper = shallow(
      <EventHeader {...mockProps}/>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
