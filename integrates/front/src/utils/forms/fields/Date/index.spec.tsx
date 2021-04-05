import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { Date } from "utils/forms/fields/Date";
import { required } from "utils/validations";

describe("Date Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Date).toStrictEqual("function");
  });

  it("should render date component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={Date}
            id={"test"}
            name={"dateTest"}
            validate={[required]}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find("input").props().id).toBe("test");
  });
});
