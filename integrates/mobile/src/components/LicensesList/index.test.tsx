import { render } from "@testing-library/react-native";
import React from "react";

import { LicensesList } from ".";

describe("LicensesList", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LicensesList).toBe("function");
  });

  it("should display licenses_list", (): void => {
    expect.hasAssertions();

    const component = render(
      <LicensesList
        licenses={[
          {
            key: "",
            licenseUrl: "",
            licenses: "",
            name: "",
            parents: "",
            repository: "",
            version: "",
          },
        ]}
      />
    );

    expect(component).toBeDefined();
  });
});
