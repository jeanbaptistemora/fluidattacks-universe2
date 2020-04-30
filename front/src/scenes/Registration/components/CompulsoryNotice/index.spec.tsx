import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { CompulsoryNotice } from "./index";

describe("Compulsory notice modal", () => {
  it("should return a function", () => {
    expect(typeof (CompulsoryNotice))
      .toEqual("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice
        content=""
        open={true}
        onAccept={jest.fn()}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render checkbox", () => {
    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice
        content=""
        open={true}
        onAccept={jest.fn()}
      />,
    );
    const checkbox: ShallowWrapper = wrapper.find("modal")
      .dive()
      .find("Field");
    expect(checkbox)
      .toHaveLength(1);
  });

  it("should submit", () => {
    const handleAccept: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <CompulsoryNotice
          content=""
          open={true}
          onAccept={handleAccept}
        />
      </Provider>,
    );
    const form: ReactWrapper = wrapper.find("modal")
      .find("genericForm");
    form.simulate("submit");
    expect(handleAccept.mock.calls.length)
      .toEqual(1);
  });
});
