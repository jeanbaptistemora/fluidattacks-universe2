import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import PhoneInput from "react-phone-input-2";
import { Provider } from "react-redux";
import { Field } from "redux-form";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import store from "store";
import { PhoneNumber } from "utils/forms/fields/PhoneNumber";
import { required } from "utils/validations";

describe("PhoneNumber Field", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof PhoneNumber).toStrictEqual("function");
  });

  it("should render phonenumber component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <GenericForm name={""} onSubmit={jest.fn()}>
          <Field
            component={PhoneNumber}
            id={"test"}
            name={"phoneTest"}
            type={"text"}
            validate={[required]}
          />
        </GenericForm>
      </Provider>
    );

    expect(wrapper.find(PhoneInput).props().country).toBe("co");
  });
});
