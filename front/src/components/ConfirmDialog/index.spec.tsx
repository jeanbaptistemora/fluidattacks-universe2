/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
import { Button } from "../Button/index";
import { ConfirmDialog, ConfirmFn } from "./index";

describe("ConfirmDialog", (): void => {

  it("should return a fuction", (): void => {
    expect(typeof (ConfirmDialog))
      .toEqual("function");
  });

  it("should handle cancel", async () => {
    const confirmCallback: jest.Mock = jest.fn();
    const cancelCallback: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <ConfirmDialog title="Title test">
        {(confirm: ConfirmFn): React.ReactNode => {
          const handleClick: (() => void) = (): void => { confirm(confirmCallback, cancelCallback); };

          return (
            <Button onClick={handleClick}>
              Test
            </Button>
          );
        }}
      </ConfirmDialog>,
    );
    const testButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Test"))
      .at(0);
    testButton.simulate("click");
    let confirmDialogModal: ReactWrapper = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Title test"});
    expect(confirmDialogModal)
      .toHaveLength(1);
    const cancelButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Cancel"))
      .at(0);
    cancelButton.simulate("click");
    confirmDialogModal = wrapper
      .find("modal")
      .find({open: true, headerTitle: "Title test"});
    expect(confirmDialogModal)
      .toHaveLength(0);
    expect(confirmCallback)
      .toHaveBeenCalledTimes(0);
    expect(cancelCallback)
      .toHaveBeenCalledTimes(1);
  });
});
