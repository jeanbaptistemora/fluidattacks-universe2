import React from "react";
import _ from "lodash";
import { default as style } from "../../index.css";
import translate from "./../../../translations/translate";
import { validTextField } from "../../../../utils/validations";
import { FormControlProps, HelpBlock } from "react-bootstrap";
import { WithContext as ReactTags, Tag } from "react-tag-input";
import { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface ITagInputProps extends WrappedFieldProps, FormControlProps {
  input: { value: string } & Omit<WrappedFieldInputProps, "value">;
  onDeletion: (tag: string) => void;
}
export const TagInput: React.FC<ITagInputProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITagInputProps>
): JSX.Element => {
  const { onDeletion, input } = props;
  const { value, onChange } = input;

  // Hooks
  const [tagsInput, setTagsInput] = React.useState<Tag[]>([]);
  const [tagsError, setTagsError] = React.useState(false);
  React.useEffect((): void => {
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
    // We only want this to run when the component mounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tagsToString: (tags: readonly Readonly<Tag>[]) => string = (
    tags: readonly Readonly<Tag>[]
  ): string => tags.map((tag: Readonly<Tag>): string => tag.text).join(",");

  function handleAddition(tag: Readonly<Tag>): void {
    if (_.isUndefined(validTextField(tag.text))) {
      setTagsInput([...tagsInput, tag]);
      onChange(tagsToString([...tagsInput, tag]));
      setTagsError(false);
    } else {
      setTagsError(true);
    }
  }
  function handleDelete(index: number): void {
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
    onDeletion(deletedTags);
    onChange(tagsToString(newTags));
  }
  function handleInputBlur(inputText: string): void {
    const tag: Tag = { id: inputText, text: inputText };
    const currentString: string = tagsToString(tagsInput);
    if (
      !_.isEmpty(inputText) &&
      !_.includes(currentString.split(","), inputText)
    ) {
      handleAddition(tag);
    }
  }

  const keyCodes: Record<string, number> = { comma: 188, enter: 13, space: 32 };
  const styles: Record<string, string> = {
    remove: style.tagRemove,
    tag: style.inputTags,
    tagInput: style.tagInput,
    tagInputField: style.formControl,
  };

  return (
    <React.Fragment>
      <ReactTags
        allowDragDrop={false}
        classNames={styles}
        delimiters={Object.values(keyCodes)}
        handleAddition={handleAddition}
        handleDelete={handleDelete}
        handleInputBlur={handleInputBlur}
        inputFieldPosition={"inline"}
        maxLength={25}
        name={"tags"}
        placeholder={""}
        tags={tagsInput}
      />
      {tagsError && (
        <HelpBlock
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          className={style.validationError}
          id={"validationError"}
        >
          {translate.t("validations.alphanumeric")}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
