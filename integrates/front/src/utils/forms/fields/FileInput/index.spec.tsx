import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { FormGroup } from "styles/styledComponents";
import { FileInput } from "utils/forms/fields/FileInput";
import { required } from "utils/validations";

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

    expect(wrapper.find(FormGroup).props().id).toBe("test");
  });
});
