import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { Dropdown } from "utils/forms/fields/Dropdown";
import { required } from "utils/validations";

describe("Dropdown Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dropdown).toStrictEqual("function");
  });

  it("should render dropdown component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={Dropdown}
            name={"dropdownTest"}
            type={"text"}
            validate={[required]}
          >
            <option value={""} />
            <option value={"test"}>{"Test"}</option>
          </Field>
        </GenericForm>
      </Provider>
    );

    const options: ReactWrapper = wrapper.find("option");

    expect(options).toHaveLength(2);
  });
});
