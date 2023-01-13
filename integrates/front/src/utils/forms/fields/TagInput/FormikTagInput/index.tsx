import type { FieldProps } from "formik";
import { useField } from "formik";
import _ from "lodash";
import type { InputHTMLAttributes } from "react";
import React, { useCallback, useEffect, useState } from "react";
import { WithContext as ReactTagInput } from "react-tag-input";
import type { Tag } from "react-tag-input";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import { validTextField } from "utils/validations";

interface ITagInputProps
  extends FieldProps<string, Record<string, string>>,
    Omit<InputHTMLAttributes<HTMLInputElement>, "form"> {
  disabled: boolean;
  placeholder: string;
  onDeletion?: (tag: string) => void;
}

export const FormikTagInput: React.FC<ITagInputProps> = (
  props: Readonly<ITagInputProps>
): JSX.Element => {
  const { disabled, onDeletion = undefined, field, form, placeholder } = props;
  const { name } = field;
  const { value }: { value: string | undefined } = field;
  const { errors, touched, setErrors } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];
  const [, , helpers] = useField(name);

  const [tagsInput, setTagsInput] = useState<Tag[]>([]);

  useEffect((): void => {
    const tags: Tag[] = value
      .split(",")
      .filter((inputTag: string): boolean => !_.isEmpty(inputTag))
      .map(
        (inputTag: string): Tag => ({
          id: inputTag.trim(),
          text: inputTag.trim(),
        })
      );
    setTagsInput(tags);
  }, [value]);

  function tagsToString(tags: Tag[]): string {
    return tags.map((tag: Readonly<Tag>): string => tag.text).join(",");
  }

  const handleAddition = useCallback(
    (tag: Readonly<Tag>): void => {
      const validation: string | undefined = validTextField(tag.text);
      if (validation === undefined) {
        setTagsInput([...tagsInput, tag]);
        helpers.setValue(tagsToString([...tagsInput, tag]));
      } else {
        setErrors({ tags: validation });
      }
    },
    [helpers, tagsInput, setErrors]
  );
  const handleDelete = useCallback(
    (index: number): void => {
      const newTags: Tag[] = tagsInput.filter(
        (_tag: Readonly<Tag>, indexFilter: number): boolean =>
          indexFilter !== index
      );
      const deletedTags: string = tagsInput.reduce(
        (
          tagValue: string,
          currentTag: Readonly<Tag>,
          indexFilter: number
        ): string => (indexFilter === index ? currentTag.text : tagValue),
        ""
      );
      setTagsInput(newTags);
      if (onDeletion !== undefined) {
        onDeletion(deletedTags);
      }
      helpers.setValue(tagsToString(newTags));
    },
    [helpers, onDeletion, tagsInput]
  );
  const handleInputBlur = useCallback(
    (inputText: string): void => {
      const tag: Tag = { id: inputText, text: inputText };
      const currentString: string = tagsToString(tagsInput);
      if (
        !_.isEmpty(inputText) &&
        !_.includes(currentString.split(","), inputText)
      ) {
        handleAddition(tag);
      }
    },
    [handleAddition, tagsInput]
  );

  const keyCodes: Record<string, number> = { comma: 188, enter: 13, space: 32 };
  const styles: Record<string, string> = {
    remove: style.tagRemove,
    tag: style.inputTags,
    tagInputField: `${style["form-control"]} pa2`,
  };

  return (
    <React.Fragment>
      <ReactTagInput
        allowDragDrop={false}
        autofocus={false}
        classNames={styles}
        delimiters={Object.values(keyCodes)}
        handleAddition={handleAddition}
        handleDelete={handleDelete}
        handleInputBlur={handleInputBlur}
        inputFieldPosition={"inline"}
        maxLength={30}
        name={name}
        placeholder={placeholder}
        readOnly={disabled}
        tags={tagsInput}
      />
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
