import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { Modal, Text } from "react-native";

import { Licenses } from ".";
import { LicensesItem } from "../LicensesItem";

describe("Licenses", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Licenses).toStrictEqual("function");
  });

  it("should display licenses", (): void => {
    expect.hasAssertions();

    const setModalVisible: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Licenses setVisible={setModalVisible} visible={true} />
    );

    expect(wrapper).toHaveLength(1);
    expect(
      wrapper.find(LicensesItem).first().find(Text).first().render().text()
    ).toStrictEqual("@apollo/client");

    const onClose: ReactWrapper<React.ComponentProps<typeof Modal>> =
      wrapper.find(Modal);

    (onClose.invoke("onRequestClose") as () => void)();

    expect(setModalVisible).toHaveBeenCalledTimes(1);
  });
});
