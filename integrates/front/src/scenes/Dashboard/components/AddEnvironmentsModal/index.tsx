import { Button } from "../../../../components/Button";
import { ButtonToolbar } from "react-bootstrap";
import { EnvironmentFields } from "./environmentFields";
import { GenericForm } from "../GenericForm";
import { IEnvironmentsAttr } from "../../containers/ProjectSettingsView/types";
import { Modal } from "../../../../components/Modal";
import React from "react";
import { translate } from "../../../../utils/translations/translate";
import { FieldArray, InjectedFormProps } from "redux-form";

interface IAddEnvironmentsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { resources: IEnvironmentsAttr[] }) => void;
}

const AddEnvironmentsModal: React.FC<IAddEnvironmentsModalProps> = (
  props: IAddEnvironmentsModalProps
): JSX.Element => {
  const { onClose, onSubmit, isOpen } = props;

  return (
    <Modal
      footer={<div />}
      headerTitle={translate.t("search_findings.tab_resources.modal_env_title")}
      open={isOpen}
    >
      <GenericForm
        initialValues={{ resources: [{ urlEnv: "" }] }}
        name={"addEnvs"}
        onSubmit={onSubmit}
      >
        {({ pristine }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <FieldArray component={EnvironmentFields} name={"resources"} />
            <ButtonToolbar bsClass={"btn-toolbar pull-right"}>
              <Button onClick={onClose}>
                {translate.t("confirmmodal.cancel")}
              </Button>
              <Button disabled={pristine} type={"submit"}>
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { IAddEnvironmentsModalProps, AddEnvironmentsModal };
