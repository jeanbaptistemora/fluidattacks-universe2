import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { Text } from "utils/forms/fields/Text";
import { required } from "utils/validations";

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
