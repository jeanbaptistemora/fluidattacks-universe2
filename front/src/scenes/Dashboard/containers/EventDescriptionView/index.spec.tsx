import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../../../store/index";
import { eventDescriptionView as EventDescriptionView, IEventDescriptionViewProps } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => JSX.Element) = (): JSX.Element => <div />;

describe("EventDescriptionView", () => {

  const mockProps: IEventDescriptionViewProps = {
    eventData: {
      accessibility: "Repositorio",
      affectation: "0",
      affectedComponents: "",
      analyst: "user@test.com",
      client: "TEST",
      clientProject: "TEST",
      detail: "This is a test",
      eventDate: "2018-10-17 00:00:00",
      eventStatus: "SOLVED",
      eventType: "AUTHORIZATION_SPECIAL_ATTACK",
      evidence: "00000000012dsasdf",
      id: "463457733",
      projectName: "TEST",
    },
    eventId: "463457733",
    formValues: {
      editEvent: {
        values: {
          accessibility: "",
        },
      },
    },
    isActiveTab: true,
    isEditable: false,
    match: {
      isExact: true,
      params: {eventId: "463457733"},
      path: "/",
      url: "",
    },
    urlDescription: functionMock,
    urlEvidence: functionMock,
  };

  it("should return a fuction", () => {
    expect(typeof (EventDescriptionView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <EventDescriptionView {...mockProps} />
      </Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
