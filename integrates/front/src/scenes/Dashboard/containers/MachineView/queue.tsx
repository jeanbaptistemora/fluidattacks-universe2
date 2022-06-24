import { Field, Form, Formik } from "formik";
import React, { useState } from "react";

import type { IQueue } from "./types";

import { ModalConfirm } from "components/Modal";
import { FormGroup } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import style from "utils/forms/index.css";
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

  function handleClose(): void {
    onClose();
  }
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
  async function handleSubmit(values: Record<string, unknown>): Promise<void> {
    setIsJobSubmitted(true);
    const nicknames = Object.keys(values).flatMap(
      (root: string): [] | [string] =>
        rootNicknames.includes(root) && values[root] === true ? [root] : []
    );
    await onSubmit(nicknames);
    onClose();
  }

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
              <ul className={style.suggestionList}>
                {rootNicknames.map((root): JSX.Element => {
                  return (
                    <Field
                      component={FormikCheckbox}
                      key={root}
                      label={root}
                      name={root}
                      type={"checkbox"}
                    />
                  );
                })}
              </ul>
              <ModalConfirm disabled={isJobSubmitted} onCancel={handleClose} />
            </FormGroup>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export { Queue };
