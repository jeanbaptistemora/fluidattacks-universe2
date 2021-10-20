import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";

import { LicensesList } from ".";

describe("LicensesList", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LicensesList).toStrictEqual("function");
  });

  it("should display licenses_list", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
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

    expect(wrapper).toHaveLength(1);
  });
});
