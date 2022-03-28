import _ from "lodash";
import React, { useCallback, useContext, useState } from "react";
import { useHotkeys } from "react-hotkeys-hook";
import { useTranslation } from "react-i18next";
import TextArea from "react-textarea-autosize";

import { Button } from "components/Button";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type { ICommentContext } from "scenes/Dashboard/components/Comments/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

import "scenes/Dashboard/components/Comments/index.css";

interface ICommentEditorProps {
  id: number;
  onPost: (editorText: string) => void;
}

const CommentEditor: React.FC<ICommentEditorProps> = ({
  id,
  onPost,
}: ICommentEditorProps): JSX.Element => {
  const { t } = useTranslation();
  const [editorText, setEditorText] = useState("");
  const { replying, setReplying }: ICommentContext = useContext(commentContext);

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

  const clickHandler: () => void = useCallback((): void => {
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

  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  useHotkeys("ctrl+enter", clickHandler, { enableOnTags: ["TEXTAREA"] });

  return (
    <React.Fragment>
      <TextArea
        aria-label={"comment-editor"}
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={true}
        maxRows={8}
        minRows={2}
        onChange={onChange}
        onFocus={onFocus}
        placeholder={t("comments.editorPlaceholder")}
        value={editorText}
      />
      <div className={"pv2"}>
        <Row>
          <Col100>
            {editorText !== "" && (
              <ButtonToolbar>
                <Button onClick={clickHandler} variant={"primary"}>
                  {t("comments.send")}
                </Button>
              </ButtonToolbar>
            )}
          </Col100>
        </Row>
      </div>
    </React.Fragment>
  );
};

export { CommentEditor };
