import { Form, Formik } from "formik";
import React, { useCallback, useState } from "react";

import type { IQueue } from "./types";

import { Checkbox } from "components/Input";
import { ModalConfirm } from "components/Modal";
import { FormGroup } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const initializeRootNicknames = (
  nicknames: string[],
  value: boolean
): Record<string, boolean> =>
  Object.fromEntries(
    new Map(
      nicknames.map((root: string): readonly [PropertyKey, boolean] => [
        root,
        value,
      ])
    )
  );

const Queue: React.FC<IQueue> = (props: Readonly<IQueue>): JSX.Element => {
  const { rootNicknames, onClose, onSubmit } = props;

  const [isJobSubmitted, setIsJobSubmitted] = useState(false);
  const [isCheckAll, setIsCheckAll] = useState(false);

  const availableRoots: Record<string, boolean> = initializeRootNicknames(
    rootNicknames,
    false
  );
  const [initialValues, setInitialValues] = useState<Record<string, boolean>>({
    ...availableRoots,
    checkAll: isCheckAll,
  });

  const handleClose = useCallback((): void => {
    onClose();
  }, [onClose]);

  function handleOnCheckAll(): void {
    setIsCheckAll(!isCheckAll);
    if (isCheckAll) {
      setInitialValues({
        ...initializeRootNicknames(rootNicknames, false),
        checkAll: false,
      });
    } else {
      setInitialValues({
        ...initializeRootNicknames(rootNicknames, true),
        checkAll: true,
      });
    }
  }
  const handleSubmit = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      setIsJobSubmitted(true);
      const nicknames = Object.keys(values).flatMap(
        (root: string): [] | [string] =>
          rootNicknames.includes(root) && values[root] === true ? [root] : []
      );
      await onSubmit(nicknames);
      onClose();
    },
    [onClose, onSubmit, rootNicknames]
  );

  return (
    <div>
      <p>{"Roots to execute"}</p>
      <Formik
        enableReinitialize={true}
        initialValues={initialValues}
        onSubmit={handleSubmit}
      >
        <Form>
          <React.Fragment>
            <input
              name={"checkAll"}
              onChange={handleOnCheckAll}
              type={"checkbox"}
            />
            {` ${translate.t("searchFindings.tabMachine.checkAll")}`}
          </React.Fragment>
          <div>
            <FormGroup>
              <br />
              {rootNicknames.map((root): JSX.Element => {
                return <Checkbox key={root} label={root} name={root} />;
              })}
              <ModalConfirm disabled={isJobSubmitted} onCancel={handleClose} />
            </FormGroup>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export { Queue };
