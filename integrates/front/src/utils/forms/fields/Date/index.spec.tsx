import { Date } from "utils/forms/fields/Date";
import { Field } from "redux-form";
import { FormControl } from "react-bootstrap";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { required } from "utils/validations";
import store from "store";

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

    expect(wrapper.find(FormControl).props().id).toBe("test");
  });
});
