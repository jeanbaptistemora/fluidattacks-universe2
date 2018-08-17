/* tslint:disable jsx-no-multiline-js
 * Disabling this rule is necessary for the sake of readability
 * of the code that renders/hides the component
 */
import PropTypes from "prop-types";
import React from "react";

interface ICommentBoxProps {
  type: string;
  visible: boolean;
}

const commentBox: React.StatelessComponent<ICommentBoxProps> =
  (props: ICommentBoxProps): JSX.Element => (
    <React.StrictMode>
      { props.visible
        ? <div id={props.type} className="tab-pane cont">
            <div id={`${props.type}s-container`}/>
          </div>
        : undefined
      }
    </React.StrictMode>
);

commentBox.propTypes = {
  type: PropTypes.string.isRequired,
  visible: PropTypes.bool.isRequired,
};

export = commentBox;
