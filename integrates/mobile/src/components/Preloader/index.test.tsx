import { render } from "@testing-library/react-native";
import React from "react";

import { Preloader } from ".";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Preloader).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const { getByTestId, queryByTestId, update } = render(
      <Preloader visible={true} />
    );

    expect(getByTestId("preloader")).toBeDefined();

    update(<Preloader visible={false} />);

    expect(queryByTestId("preloader")).toBeNull();
  });
});
