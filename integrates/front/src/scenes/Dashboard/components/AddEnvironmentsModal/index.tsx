import { Button } from "components/Button";
import { ButtonToolbar } from "styles/styledComponents";
import { EnvironmentFields } from "scenes/Dashboard/components/AddEnvironmentsModal/environmentFields";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { IEnvironmentsAttr } from "scenes/Dashboard/containers/ProjectSettingsView/types";
import { Modal } from "components/Modal";
import React from "react";
import { translate } from "utils/translations/translate";
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
            <ButtonToolbar>
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
