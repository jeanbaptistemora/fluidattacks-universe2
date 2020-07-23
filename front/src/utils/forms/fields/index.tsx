import _ from "lodash";
import React from "react";
import { FormControlProps,  HelpBlock } from "react-bootstrap";
import { Tag, WithContext as ReactTags } from "react-tag-input";
import { WrappedFieldProps } from "redux-form";
import { validTextField } from "../../../utils/validations";
import { default as style } from "../index.css";
import translate from "./../../translations/translate";

type CustomFieldProps = WrappedFieldProps & FormControlProps;

const renderError: ((arg1: string) => JSX.Element) = (msg: string): JSX.Element => (
  <HelpBlock id="validationError" className={style.validationError}>{msg}</HelpBlock>
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

export { AutoCompleteText } from "./AutoCompleteText";
export { Text } from "./Text";
export { PhoneNumber } from "./PhoneNumber";
export { Dropdown } from "./Dropdown";
export { TextArea } from "./TextArea";
export { Date } from "./Date";
export { FileInput } from "./FileInput";
export { DateTime } from "./DateTime";
export { Checkbox } from "./Checkbox";
export { SwitchButton } from "./SwitchButton";
