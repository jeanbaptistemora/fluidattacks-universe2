import { fireEvent, render, screen } from "@testing-library/react-native";
import React from "react";
import { Linking } from "react-native";

import { Link } from ".";

describe("Link", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Link).toBe("function");
  });

  it("should display", (): void => {
    expect.hasAssertions();

    /* eslint-disable-next-line react/forbid-component-props */
    render(<Link style={{}}>{"test"}</Link>);

    expect(screen.getByText("test")).toBeDefined();
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
      /* eslint-disable-next-line react/forbid-component-props */
      <Link style={{}} url={""}>
        {"test"}
      </Link>
    );

    expect(screen.getByText("test")).toBeDefined();

    fireEvent(screen.getByText("test"), "onPress");

    expect(Linking.openURL).toHaveBeenCalledTimes(1);
  });
});
