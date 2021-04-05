import { Form, Input } from "antd";
import React, { useCallback, useState } from "react";

import { Button } from "components/Button";
import { translate } from "utils/translations/translate";

const { TextArea } = Input;

interface ICommentEditorProps {
  onPost: (editorText: string) => void;
}

const CommentEditor: React.FC<ICommentEditorProps> = (
  props: ICommentEditorProps
): JSX.Element => {
  const { onPost } = props;
  const [editorText, setEditorText] = useState("");

  const onChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
      setEditorText(event.target.value);
    },
    []
  );

  const clickHandler: () => void = useCallback((): void => {
    if (editorText !== "") {
      onPost(editorText);
      setEditorText("");
    }
  }, [editorText, onPost]);

  return (
    <React.Fragment>
      <Form.Item>
        <TextArea
          allowClear={true}
          onChange={onChange}
          rows={4}
          value={editorText}
        />
      </Form.Item>
      <Form.Item>
        <Button onClick={clickHandler}>{translate.t("comments.send")}</Button>
      </Form.Item>
    </React.Fragment>
  );
};

export { CommentEditor };
