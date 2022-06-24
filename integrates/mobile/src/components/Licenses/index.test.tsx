import { fireEvent, render } from "@testing-library/react-native";
import React from "react";

import { Licenses } from ".";

describe("Licenses", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Licenses).toBe("function");
  });

  it("should display licenses", (): void => {
    expect.hasAssertions();

    const setModalVisible: jest.Mock = jest.fn();
    const { getByLabelText } = render(
      <Licenses setVisible={setModalVisible} visible={true} />
    );

    expect(getByLabelText("licenses-info")).toBeDefined();

    fireEvent(getByLabelText("licenses-info"), "onRequestClose");

    expect(setModalVisible).toHaveBeenCalledTimes(1);
  });
});
