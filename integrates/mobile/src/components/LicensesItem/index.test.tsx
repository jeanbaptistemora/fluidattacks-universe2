import { fireEvent, render, screen } from "@testing-library/react-native";
import React from "react";
import { Linking } from "react-native";

import { LicensesItem } from ".";

describe("LicensesItem", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LicensesItem).toBe("function");
  });

  it("should display and mock open_url", (): void => {
    expect.hasAssertions();

    interface IOpenURLMock {
      openURL: jest.Mock<Promise<string>, []>;
    }
    jest.mock(
      "react-native/Libraries/Linking/Linking",
      (): IOpenURLMock => ({
        openURL: jest.fn(
          async (): Promise<string> => Promise.resolve("mockResolve")
        ),
      })
    );

    render(
      <LicensesItem
        licenseUrl={"https://test-url.com/"}
        licenses={"test"}
        name={"@test-library@1.0"}
        repository={"https://test-url.com/"}
        version={"1.0"}
      />
    );

    expect(screen.getByText("@test-library@1.0")).toBeDefined();

    fireEvent(screen.getByText("@test-library@1.0"), "onPress");

    expect(Linking.openURL).toHaveBeenCalledTimes(1);
  });
});
