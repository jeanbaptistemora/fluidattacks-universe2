/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { useArgs } from "@storybook/addons";
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React, { useCallback } from "react";

import type { IModalProps } from ".";
import { Modal, ModalFooter } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: Modal,
  title: "Components/Modal",
};

const Template: Story<PropsWithChildren<IModalProps>> = (
  props
): JSX.Element => {
  const [, setArgs] = useArgs();
  const openModal = useCallback((): void => {
    setArgs({ open: true });
  }, [setArgs]);
  const closeModal = useCallback((): void => {
    setArgs({ open: false });
  }, [setArgs]);

  return (
    <React.Fragment>
      <Button onClick={openModal} variant={"primary"}>
        {"Open modal"}
      </Button>
      <Modal {...props} onClose={closeModal}>
        <p>{"Modal body goes here"}</p>
        <ModalFooter>
          <Button variant={"secondary"}>{"Secondary button"}</Button>
          <Button variant={"primary"}>{"Primary button"}</Button>
        </ModalFooter>
      </Modal>
    </React.Fragment>
  );
};

const Default = Template.bind({});
Default.args = {
  open: false,
  title: "Test title",
};

export { Default };
export default config;
