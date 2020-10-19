import { Button } from "components/Button";
import { ConfigurableValidator } from "revalidate";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types.ts";
import { Modal } from "components/Modal";
import React from "react";
import { renderUploadBar } from "scenes/Dashboard/components/AddFilesModal/renderUploadBar";
import { translate } from "utils/translations/translate";
import { ButtonToolbar, RequiredField } from "styles/styledComponents";
import { Field, InjectedFormProps, Validator } from "redux-form";
import { FileInput, TextArea } from "utils/forms/fields";
import {
  isValidFileName,
  isValidFileSize,
  maxLength,
  required,
  validField,
  validTextField,
} from "utils/validations";

const MAX_LENGTH: number = 200;
const maxFileDescriptionLength: ConfigurableValidator = maxLength(MAX_LENGTH);

const addFilesModal: React.FC<IAddFilesModalProps> = (
  props: IAddFilesModalProps
): JSX.Element => {
  const { isOpen, isUploading, onClose, onSubmit } = props;

  const MAX_FILE_SIZE: number = 100;
  const maxFileSize: Validator = isValidFileSize(MAX_FILE_SIZE);

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "search_findings.tab_resources.modal_file_title"
        )}
        open={isOpen}
      >
        <GenericForm name={"addFiles"} onSubmit={onSubmit}>
          {({ pristine }: InjectedFormProps): React.ReactNode => (
            <React.Fragment>
              <div>
                <div>
                  <label>
                    <RequiredField>{"*"} </RequiredField>
                    {translate.t("validations.file_size", { count: 100 })}
                  </label>
                  <Field
                    component={FileInput}
                    id={"file"}
                    name={"file"}
                    validate={[required, isValidFileName, maxFileSize]}
                  />
                </div>
                <div>
                  <label>
                    <RequiredField>{"*"} </RequiredField>
                    {translate.t("search_findings.tab_resources.description")}
                  </label>
                  <Field
                    component={TextArea}
                    name={"description"}
                    type={"text"}
                    validate={[
                      required,
                      validField,
                      maxFileDescriptionLength,
                      validTextField,
                    ]}
                  />
                </div>
              </div>
              {isUploading ? renderUploadBar(props) : undefined}
              <br />
              <ButtonToolbar>
                <Button disabled={isUploading} onClick={onClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button disabled={pristine || isUploading} type={"submit"}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { IAddFilesModalProps, addFilesModal as AddFilesModal };
