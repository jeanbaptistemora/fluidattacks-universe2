/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that renders the footer
 *
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */

import React from "react";
import { Button, ButtonToolbar, Row } from "react-bootstrap";
import translate from "../../utils/translations/translate";
import { default as Modal } from "../Modal/index";

export interface IConfirmDialogProps {
  open: boolean;
  title: string;
  onCancel?(): void;
  onProceed(): void;
}

export const confirmDialog: React.SFC<IConfirmDialogProps> = (props: IConfirmDialogProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      headerTitle={props.title}
      open={props.open}
      content={<p>{translate.t("confirmmodal.message")}</p>}
      footer={
        <Row>
          <ButtonToolbar className="pull-right">
            <Button
              onClick={(): void => { if (props.onCancel !== undefined) { props.onCancel(); }}}
            >
              {translate.t("confirmmodal.cancel")}
            </Button>
            <Button
              bsStyle="primary"
              onClick={(): void => { props.onProceed(); }}
            >
              {translate.t("confirmmodal.proceed")}
            </Button>
          </ButtonToolbar>
        </Row>
      }

    />
  </React.StrictMode>
);
