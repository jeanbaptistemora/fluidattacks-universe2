/* tslint:disable:jsx-no-lambda
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import React from "react";
import { Checkbox } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { default as Modal } from "../../../../components/Modal/index";
import translate from "../../../../utils/translations/translate";

/**
 *  CompulsoryNotice properties
 */
export interface ICompulsoryNoticeProps {
  content: string;
  id: string;
  open: boolean;
  rememberDecision: boolean;
  onAccept(rememberValue: boolean): void;
  onCheckRemember(): void;
}

const modalContent: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <div>
    <p>{props.content}</p>
    <p title={translate.t("legalNotice.rememberCbo.tooltip")}>
      <Checkbox
        checked={props.rememberDecision}
        onClick={(): void => { props.onCheckRemember(); }}
      >
        {translate.t("legalNotice.rememberCbo.text")}
      </Checkbox>
    </p>
  </div>
);

const modalFooter: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <Button
    bsStyle="primary"
    title={translate.t("legalNotice.acceptBtn.tooltip")}
    onClick={(): void => { props.onAccept(props.rememberDecision); }}
  >
    {translate.t("legalNotice.acceptBtn.text")}
  </Button>
);

/**
 * CompulsoryNotice component
 */
export const compulsoryNotice: React.SFC<ICompulsoryNoticeProps> =
  (props: ICompulsoryNoticeProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      open={props.open}
      headerTitle={translate.t("legalNotice.title")}
      content={modalContent(props)}
      footer={modalFooter(props)}
    />
  </React.StrictMode>
);
