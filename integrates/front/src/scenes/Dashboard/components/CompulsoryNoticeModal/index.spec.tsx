import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";

import { CompulsoryNotice } from "scenes/Dashboard/components/CompulsoryNoticeModal";
import store from "store";

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
    const checkbox: ShallowWrapper = wrapper.find("Modal").dive().find("Field");

    expect(checkbox).toHaveLength(1);
  });

  it("should submit", async (): Promise<void> => {
    expect.hasAssertions();

    const handleAccept: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <CompulsoryNotice content={""} onAccept={handleAccept} open={true} />
      </Provider>
    );
    const form: ReactWrapper = wrapper.find("Modal").find("Formik");
    await act(async (): Promise<void> => {
      form.simulate("submit");

      await wait(0);
      wrapper.update();
    });

    expect(handleAccept.mock.calls).toHaveLength(1);
  });
});
