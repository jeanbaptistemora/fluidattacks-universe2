import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { Text } from "utils/forms/fields/Text";
import { mount } from "enzyme";
import { required } from "utils/validations";
import store from "store";

describe("Text Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Text).toStrictEqual("function");
  });

  it("should render text component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={Text}
            id={"test"}
            name={"textTest"}
            type={"text"}
            validate={[required]}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find("input").props().id).toBe("test");
  });
});
