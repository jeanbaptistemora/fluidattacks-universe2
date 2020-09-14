import { Field } from "redux-form";
import { FormControl } from "react-bootstrap";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import { Text } from "utils/forms/fields/Text";
import { required } from "utils/validations";
import store from "store";
import { ReactWrapper, mount } from "enzyme";

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

    expect(wrapper.find(FormControl).props().id).toBe("test");
  });
});
