import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
import { Button } from "../Button/index";
import { ConfirmDialog, ConfirmFn } from "./index";

describe("ConfirmDialog", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof ConfirmDialog).toStrictEqual("function");
  });

  it("should handle cancel", (): void => {
    expect.hasAssertions();
    const confirmCallback: jest.Mock = jest.fn();
    const cancelCallback: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <ConfirmDialog title={"Title test"}>
        {(confirm: ConfirmFn): React.ReactNode => {
          function handleClick(): void {
            confirm(confirmCallback, cancelCallback);
          }

          return <Button onClick={handleClick}>{"Test"}</Button>;
        }}
      </ConfirmDialog>
    );

    const testButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: Readonly<ReactWrapper>): boolean =>
        element.contains("Test")
      )
      .at(0);
    testButton.simulate("click");
    const confirmDialogModal: ReactWrapper = wrapper
      .find("modal")
      .find({ open: true, headerTitle: "Title test" });
    const cancelButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: Readonly<ReactWrapper>): boolean =>
        element.contains("Cancel")
      )
      .at(0);
    cancelButton.simulate("click");
    const confirmDialogModalAfterClickCancel: ReactWrapper = wrapper
      .find("modal")
      .find({ open: true, headerTitle: "Title test" });

    expect(confirmDialogModal).toHaveLength(1);
    expect(confirmDialogModalAfterClickCancel).toHaveLength(0);
    expect(confirmCallback).toHaveBeenCalledTimes(0);
    expect(cancelCallback).toHaveBeenCalledTimes(1);
  });
});
