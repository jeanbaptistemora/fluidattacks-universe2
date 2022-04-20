import { Field, Form, Formik } from "formik";
import type { FormikProps } from "formik";
import _ from "lodash";
import React, { useCallback, useContext, useRef, useState } from "react";
import { useHotkeys } from "react-hotkeys-hook";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type { ICommentContext } from "scenes/Dashboard/components/Comments/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { FormikTextAreaAutosize } from "utils/forms/fields/TextArea";
import { maxLength } from "utils/validations";

interface ICommentEditorProps {
  id: number;
  onPost: (editorText: string) => void;
}

const MAX_LENGTH: number = 20000;
const maxContentLength: ConfigurableValidator = maxLength(MAX_LENGTH);
const CommentEditor: React.FC<ICommentEditorProps> = ({
  id,
  onPost,
}: ICommentEditorProps): JSX.Element => {
  const { t } = useTranslation();
  const [editorText, setEditorText] = useState("");
  const { replying, setReplying }: ICommentContext = useContext(commentContext);
  const formRef = useRef<FormikProps<{ "comment-editor": string }>>(null);

  const onChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
      setEditorText(event.target.value);
      if (!_.isUndefined(setReplying)) {
        setReplying(id);
      }
    },
    [id, setReplying]
  );

  const onFocus = useCallback((): void => {
    if (!_.isUndefined(setReplying)) {
      setReplying(id);
    }
  }, [id, setReplying]);

  const clickHandler = useCallback((): void => {
    if (replying !== id) {
      setEditorText("");

      return;
    }
    const trimmedText = _.trim(editorText);
    if (trimmedText !== "") {
      onPost(trimmedText);
      setEditorText("");
    }
  }, [editorText, id, onPost, replying]);

  const onSubmit = useCallback((): void => {
    if (formRef.current !== null) {
      formRef.current.handleSubmit();
    }
  }, [formRef]);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  useHotkeys("ctrl+enter", onSubmit, { enableOnTags: ["TEXTAREA"] });

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ "comment-editor": editorText }}
      innerRef={formRef}
      name={"addConsult"}
      onSubmit={clickHandler}
    >
      <Form>
        <Row>
          <Field
            component={FormikTextAreaAutosize}
            maxRows={8}
            minRows={2}
            name={"comment-editor"}
            onFocus={onFocus}
            onTextChange={onChange}
            placeholder={t("comments.editorPlaceholder")}
            rows={"2"}
            type={"text"}
            validate={maxContentLength}
          />
        </Row>
        <div className={"pv2"}>
          <Row>
            <Col100>
              {editorText !== "" && (
                <ButtonToolbar>
                  <Button type={"submit"} variant={"primary"}>
                    {t("comments.send")}
                  </Button>
                </ButtonToolbar>
              )}
            </Col100>
          </Row>
        </div>
      </Form>
    </Formik>
  );
};

export { CommentEditor };
