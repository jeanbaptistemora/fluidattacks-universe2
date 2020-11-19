import { CompulsoryNotice } from "scenes/Registration/components/CompulsoryNotice";
import { Provider } from "react-redux";
import React from "react";
import store from "store";
import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";

describe("Compulsory notice modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof CompulsoryNotice).toStrictEqual("function");
  });

  it("should be rendered", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice content={""} onAccept={jest.fn()} open={true} />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render checkbox", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <CompulsoryNotice content={""} onAccept={jest.fn()} open={true} />
    );
    const checkbox: ShallowWrapper = wrapper.find("modal").dive().find("Field");

    expect(checkbox).toHaveLength(1);
  });

  it("should submit", (): void => {
    expect.hasAssertions();

    const handleAccept: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <CompulsoryNotice content={""} onAccept={handleAccept} open={true} />
      </Provider>
    );
    const form: ReactWrapper = wrapper.find("modal").find("genericForm");
    form.simulate("submit");

    expect(handleAccept.mock.calls).toHaveLength(1);
  });
});
