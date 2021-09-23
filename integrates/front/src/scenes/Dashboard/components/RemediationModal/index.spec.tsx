import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";

const functionMock: () => void = (): void => undefined;

describe("Remediation modal", (): void => {
  const wrapper: ShallowWrapper = shallow(
    <RemediationModal
      isLoading={false}
      isOpen={true}
      message={"test"}
      onClose={functionMock}
      onSubmit={functionMock}
      title={"title"}
    />
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RemediationModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });
});
