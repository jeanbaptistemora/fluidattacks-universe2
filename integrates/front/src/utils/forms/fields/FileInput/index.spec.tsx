import { Field } from "redux-form";
import { FileInput } from "utils/forms/fields/FileInput";
import { FormGroup } from "react-bootstrap";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Provider } from "react-redux";
import React from "react";
import { required } from "utils/validations";
import store from "store";
import { ReactWrapper, mount } from "enzyme";

describe("FileInput Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FileInput).toStrictEqual("function");
  });

  it("should render fileinput component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={FileInput}
            id={"test"}
            name={"fileInputTest"}
            validate={[required]}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find(FormGroup).props().controlId).toBe("test");
  });
});
