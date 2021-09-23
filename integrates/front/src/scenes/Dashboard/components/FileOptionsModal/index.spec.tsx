import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";

const functionMock: () => void = (): void => undefined;

describe("Add resources modal", (): void => {
  const wrapper: ShallowWrapper = shallow(
    <FileOptionsModal
      canRemove={true}
      fileName={""}
      isOpen={true}
      onClose={functionMock}
      onDelete={functionMock}
      onDownload={functionMock}
    />
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FileOptionsModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });
});
