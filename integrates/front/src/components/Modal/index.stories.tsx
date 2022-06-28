/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import { useArgs } from "@storybook/addons";
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React, { useCallback, useState } from "react";

import type { IModalProps } from ".";
import { Modal, ModalConfirm } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: Modal,
  subcomponents: { ModalConfirm },
  title: "components/Modal",
};

const Template: Story<PropsWithChildren<IModalProps>> = (
  props
): JSX.Element => {
  const [, setArgs] = useArgs();
  const [count, setCount] = useState(0);
  const openModal = useCallback((): void => {
    setArgs({ open: true });
  }, [setArgs]);
  const closeModal = useCallback((): void => {
    setArgs({ open: false });
  }, [setArgs]);
  const onConfirm = useCallback((): void => {
    setCount(count + 1);
  }, [count, setCount]);

  return (
    <React.Fragment>
      <Button onClick={openModal} variant={"primary"}>
        {"Open modal"}
      </Button>
      <Modal {...props} onClose={closeModal}>
        <p>{"Modal body goes here"}</p>
        <p>{`Count: ${count}`}</p>
        <ModalConfirm onCancel={closeModal} onConfirm={onConfirm} />
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
