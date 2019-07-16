import React from "react";
import { Checkbox } from "react-bootstrap";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
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

const modalContent: ((arg1: ICompulsoryNoticeProps) => JSX.Element) = (props: ICompulsoryNoticeProps): JSX.Element => {
  const handleRememberClick: (() => void) = (): void => { props.onCheckRemember(); };

  return (
    <div>
      <p>{props.content}</p>
      <p title={translate.t("legalNotice.rememberCbo.tooltip")}>
        <Checkbox checked={props.rememberDecision} onClick={handleRememberClick}>
          {translate.t("legalNotice.rememberCbo.text")}
        </Checkbox>
      </p>
    </div>
  );
};

const modalFooter: ((arg1: ICompulsoryNoticeProps) => JSX.Element) = (props: ICompulsoryNoticeProps): JSX.Element => {
  const handleAcceptClick: (() => void) = (): void => { props.onAccept(props.rememberDecision); };

  return (
    <Button bsStyle="primary" title={translate.t("legalNotice.acceptBtn.tooltip")} onClick={handleAcceptClick}>
      {translate.t("legalNotice.acceptBtn.text")}
    </Button>
  );
};

/**
 * CompulsoryNotice component
 */
export const compulsoryNotice: React.FC<ICompulsoryNoticeProps> = (props: ICompulsoryNoticeProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      open={props.open}
      headerTitle={translate.t("legalNotice.title")}
      content={modalContent(props)}
      footer={modalFooter(props)}
    />
  </React.StrictMode>
);
