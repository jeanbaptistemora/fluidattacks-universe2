import BootstrapSwitchButton from "bootstrap-switch-button-react";
import _ from "lodash";
import React from "react";
import {
  Badge, Checkbox, ControlLabel, FormControl, FormControlProps, FormGroup, Glyphicon, HelpBlock, InputGroup,
} from "react-bootstrap";
import { default as Datetime } from "react-datetime";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that react-datetime needs
 * to display properly even if some of them are overridden later
 */
import "react-datetime/css/react-datetime.css";
import { Tag, WithContext as ReactTags } from "react-tag-input";
import { WrappedFieldProps } from "redux-form";
import { validTextField } from "../../../utils/validations";
import { default as style } from "../index.css";
import translate from "./../../translations/translate";

type CustomFieldProps = WrappedFieldProps & FormControlProps;

const renderError: ((arg1: string) => JSX.Element) = (msg: string): JSX.Element => (
  <HelpBlock id="validationError" className={style.validationError}>{msg}</HelpBlock>
);

const renderCharacterCount: ((text: string) => JSX.Element) = (text: string): JSX.Element => (
  <Badge pullRight={true} className={style.badge}>{text.length}</Badge>
);

type tagFieldProps = CustomFieldProps & { onDeletion(tag: string): void };
export const tagInputField: React.FC<tagFieldProps> =
  (fieldProps: tagFieldProps): JSX.Element => {
    const tagsEmpty: Tag[] = [];
    const { onDeletion } = fieldProps;
    const [tagsInput, setTagsInput] = React.useState(tagsEmpty);
    const [tagsError, setTagsError] = React.useState(false);

    const onMount: (() => void) = (): void => {
      const tags: Tag[] = fieldProps.input.value.split(",")
        .filter((inputTag: string) => !_.isEmpty(inputTag))
        .map((inputTag: string) => ({ id: inputTag.trim(), text: inputTag.trim() }));
      setTagsInput(tags);
    };
    React.useEffect(onMount, []);

    const tagToString: ((tags: Tag[]) => string) = (tags: Tag[]): string => (
      tags.map((tag: Tag) => tag.text)
        .join(","));

    const handleAddition: ((tag: Tag) => void) = (tag: Tag): void => {
      if (validTextField(tag.text) === undefined) {
        setTagsInput([...tagsInput, tag]);
        const newTag: string = tagToString([...tagsInput, tag]);
        fieldProps.input.onChange(newTag);
        fieldProps.input.value = newTag;
        setTagsError(false);
      } else {
        setTagsError(true);
      }
    };
    const handleDelete: ((index: number) => void) = (index: number): void => {
      let newTags: Tag[] = tagsInput;
      newTags = newTags.filter((_0: Tag, indexFilter: number) => indexFilter !== index);
      const deletedTags: string = tagsInput.reduce(
        (tagValue: string, currentTag: Tag, indexFilter: number) =>
          (indexFilter === index ? currentTag.text : tagValue),
        "");
      setTagsInput(newTags);
      onDeletion(deletedTags);
      const newTag: string = tagToString(newTags);
      fieldProps.input.onChange(newTag);
      fieldProps.input.value = newTag;
    };
    const handleInputBlur: ((inputText: string) => void) = (inputText: string): void => {
      const tag: Tag = { id: inputText, text: inputText };
      const currentString: string = tagToString(tagsInput);
      if (!_.isEmpty(inputText) && !_.includes(currentString.split(","), inputText)) {
        handleAddition(tag);
      }
    };
    const keyCodes: Dictionary<number> = { comma: 188, enter: 13, space: 32 };
    const styles: Dictionary<string> = {
      remove: style.tagRemove, tag: style.inputTags, tagInput: style.tagInput, tagInputField: style.formControl,
    };

    return (
      <div>
        <ReactTags
          allowDragDrop={false}
          classNames={styles}
          delimiters={Object.values(keyCodes)}
          handleDelete={handleDelete}
          handleAddition={handleAddition}
          handleInputBlur={handleInputBlur}
          inputFieldPosition="inline"
          maxLength={25}
          name="tags"
          placeholder=""
          tags={tagsInput}
        />
        {tagsError ? renderError(translate.t("validations.alphanumeric")) : undefined}
      </div>
    );
  };

export const fileInputField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => {
  const handleFileChange: React.FormEventHandler<FormControl> = (event: React.FormEvent<FormControl>): void => {
    const files: FileList | null = (event.target as HTMLInputElement).files;
    fieldProps.input.onChange(_.isEmpty(files) ? [] : (files as FileList));
  };

  const selectedFile: FileList = fieldProps.input.value;

  return (
    <FormGroup controlId={fieldProps.id}>
      <InputGroup>
        <FormControl
          target={fieldProps.target}
          className={`${style.inputfile} ${style.inputfile_evidence}`}
          type="file"
          accept={fieldProps.accept}
          name={fieldProps.name}
          onChange={handleFileChange}
          onClick={fieldProps.onClick}
        />
        <ControlLabel>
          <span>{_.isEmpty(selectedFile) ? "" : selectedFile[0].name}</span>
          <strong>
            <Glyphicon glyph="search" /> Explore&hellip;
          </strong>
        </ControlLabel>
      </InputGroup>
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </FormGroup>
  );
};

export const dateField: React.FC<CustomFieldProps> =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        className={style.formControl}
        id={fieldProps.id}
        type={"date"}
        selected={fieldProps.input.value}
        onChange={fieldProps.input.onChange}
        onBlur={fieldProps.input.onBlur}
        disabled={fieldProps.disabled}
        value={fieldProps.input.value.split(" ")[0]}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

export const dateTimeField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => (
  <React.Fragment>
    <Datetime inputProps={{ className: style.formControl }} utc={false} {...fieldProps.input} />
    {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
  </React.Fragment>
);

export const checkboxField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => (
  <React.Fragment>
    <Checkbox checked={fieldProps.input.value} children={fieldProps.children} {...fieldProps.input} />
    {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
  </React.Fragment>
);

export interface ISwitchButtonProps extends React.ComponentProps<typeof BootstrapSwitchButton> {
  input: {
    // Redux-form managed value
    checked: boolean;
    // Redux-form onChange function, required to alter the state
    onChange(checked: boolean): void;
  };
}

// Custom BootstrapSwitchButton whose state can be managed by redux-form
export const switchButton: React.FC<ISwitchButtonProps> = (props: ISwitchButtonProps): JSX.Element => {
  const onChange: (checked: boolean) => void = (checked: boolean): void => {
    props.input.onChange(checked);
    if (!_.isUndefined(props.onChange)) {
      props.onChange(checked);
    }
  };

  return (
    <BootstrapSwitchButton
      checked={props.input.checked}
      disabled={props.disabled}
      onChange={onChange}
      offlabel={props.offlabel}
      onlabel={props.onlabel}
      onstyle={props.onstyle}
      style={props.style}
    />
  );
};

export { AutoCompleteText } from "./AutoCompleteText";
export { Text } from "./Text";
export { PhoneNumber } from "./PhoneNumber";
export { Dropdown } from "./Dropdown";
export { TextArea } from "./TextArea";
