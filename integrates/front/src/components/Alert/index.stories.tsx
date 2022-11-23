/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React, { Fragment, useCallback } from "react";

import type { IAlertProps, IToastProps } from ".";
import { Alert, ToastBox, toast } from ".";
import { Button } from "components/Button";

const config: Meta = {
  component: Alert,
  title: "components/Alert",
};

const StoryDefault: Story<PropsWithChildren<IAlertProps>> = (
  props
): JSX.Element => <Alert {...props} />;

const Default = StoryDefault.bind({});
Default.args = {
  children: "Test",
  variant: "success",
};

const StoryToast: Story<IToastProps> = (): JSX.Element => {
  const onError = useCallback((): void => {
    toast({
      msg: "Error message",
      title: "Error title!",
      variant: "error",
    });
  }, []);
  const onInfo = useCallback((): void => {
    toast({
      msg: "Info message",
      title: "Info title!",
      variant: "info",
    });
  }, []);
  const onSuccess = useCallback((): void => {
    toast({
      msg: "Success message",
      title: "Success title!",
      variant: "success",
    });
  }, []);
  const onWarning = useCallback((): void => {
    toast({
      msg: "Warning message",
      title: "Warning title!",
      variant: "warning",
    });
  }, []);

  return (
    <Fragment>
      <ToastBox autoClose={5000} position={"top-right"} />
      <Button onClick={onError}>{"Error"}</Button>
      <Button onClick={onInfo}>{"Info"}</Button>
      <Button onClick={onSuccess}>{"Success"}</Button>
      <Button onClick={onWarning}>{"Warning"}</Button>
    </Fragment>
  );
};

const Toast = StoryToast.bind({});

export { Default, Toast };
export default config;
