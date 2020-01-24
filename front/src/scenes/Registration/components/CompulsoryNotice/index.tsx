import React from "react";
import { ButtonToolbar } from "react-bootstrap";
import { Field } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { checkboxField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../../Dashboard/components/GenericForm";

/**
 *  CompulsoryNotice properties
 */
interface ICompulsoryNoticeProps {
  content: string;
  open: boolean;
  onAccept(remember: boolean): void;
}

const compulsoryNotice: React.FC<ICompulsoryNoticeProps> = (props: ICompulsoryNoticeProps): JSX.Element => {
  const handleSubmit: ((values: { remember: boolean }) => void) = (values: { remember: boolean }): void => {
    props.onAccept(values.remember);
  };

  return (
    <React.StrictMode>
      <Modal
        open={props.open}
        headerTitle={translate.t("legalNotice.title")}
        footer={<div />}
      >
        <GenericForm name="acceptLegal" initialValues={{ remember: false }} onSubmit={handleSubmit}>
          <React.Fragment>
            <p>{props.content}</p>
            <Field title={translate.t("legalNotice.rememberCbo.tooltip")} component={checkboxField} name="remember">
              {translate.t("legalNotice.rememberCbo.text")}
            </Field>
            <ButtonToolbar className="pull-right">
              <Button type="submit" title={translate.t("legalNotice.acceptBtn.tooltip")}>
                {translate.t("legalNotice.acceptBtn.text")}
              </Button>
            </ButtonToolbar>
          </React.Fragment>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { compulsoryNotice as CompulsoryNotice };
