import { Button } from "components/Button";
import type { IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import { authContext } from "utils/auth";
import moment from "moment";
import { translate } from "utils/translations/translate";
import { Form, Input } from "antd";
import type { ICommentStructure, IPostCallback } from "../Comments/types";
import React, { useCallback, useContext, useState } from "react";

const { TextArea } = Input;

interface ICommentEditorProps {
  onPostComment: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void;
}

const getFormattedTime = (): string => {
  const now = new Date();

  return moment(now).format("YYYY/MM/DD HH:mm:ss");
};

const CommentEditor: React.FC<ICommentEditorProps> = (
  props: ICommentEditorProps
): JSX.Element => {
  const { onPostComment } = props;
  const { userEmail, userName }: IAuthContext = useContext(authContext);
  const [editorText, setEditorText] = useState("");

  const onChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
      setEditorText(event.target.value);
    },
    []
  );

  const clickHandler: () => void = useCallback((): void => {
    onPostComment(
      {
        content: editorText,
        created: getFormattedTime(),
        // eslint-disable-next-line camelcase  -- Name required by the API
        created_by_current_user: true,
        email: userEmail,
        fullname: userName,
        id: 0,
        modified: getFormattedTime(),
        parent: Number("0"),
      },
      (result: ICommentStructure): void => {
        Logger.warning("There was an error posting the comment", result);
      }
    );
  }, [editorText, onPostComment, userEmail, userName]);

  return (
    <React.Fragment>
      <Form.Item>
        <TextArea onChange={onChange} rows={4} />
      </Form.Item>
      <Form.Item>
        <Button onClick={clickHandler}>{translate.t("comments.send")}</Button>
      </Form.Item>
    </React.Fragment>
  );
};

export { CommentEditor };
