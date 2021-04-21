import _ from "lodash";
import React, { useCallback, useState } from "react";
import TextArea from "react-textarea-autosize";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";
import "scenes/Dashboard/components/CommentsRefac/index.css";

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
    const trimmedText = _.trim(editorText);
    if (trimmedText !== "") {
      onPost(trimmedText);
      setEditorText("");
    }
  }, [editorText, onPost]);

  return (
    <React.Fragment>
      <TextArea
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={true}
        maxRows={8}
        minRows={2}
        onChange={onChange}
        placeholder={translate.t("comments.editorPlaceholder")}
        value={editorText}
      />
      <div className={"pv2"}>
        <Row>
          <Col100>
            {editorText !== "" && (
              <ButtonToolbar>
                <Button onClick={clickHandler}>
                  {translate.t("comments.send")}
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
