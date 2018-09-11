/* tslint:disable:jsx-no-lambda
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import PropTypes from "prop-types";
import React from "react";
import ReactReponsiveModal from "react-responsive-modal";
import globalStyle from "../../styles/global.css";
import style from "./index.css";

interface IModalProps {
  content: React.ReactNode;
  footer: React.ReactNode;
  headerTitle: string;
  open: boolean;
  onClose(): void;
}

const modal: React.StatelessComponent<IModalProps> =
  (props: IModalProps): JSX.Element => (
    <React.StrictMode>
      <ReactReponsiveModal
        open={props.open}
        onClose={(): void => { props.onClose(); }}
        classNames={{ overlay: style.overlay, modal: style.dialog }}
        closeOnEsc={false}
        closeOnOverlayClick={false}
        showCloseIcon={false}
        center={true}
      >
        <div className={style.content}>
          <div className={style.header}>
            <h3 className={globalStyle.title}>{props.headerTitle}</h3>
          </div>
          <div className={style.body}>
            {props.content}
          </div>
          <div className={style.footer}>
            {props.footer}
          </div>
        </div>
      </ReactReponsiveModal>
    </React.StrictMode>
);

modal.propTypes = {
  content: PropTypes.node.isRequired,
  footer: PropTypes.node.isRequired,
  headerTitle: PropTypes.string.isRequired,
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
};

export = modal;
