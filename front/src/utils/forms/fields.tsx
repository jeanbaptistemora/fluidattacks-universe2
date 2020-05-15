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
import PhoneInput, { PhoneInputProps } from "react-phone-input-2";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Necessary to import react-phone-input-2 default styles
 */
import "react-phone-input-2/lib/bootstrap.css";
import { Tag, WithContext as ReactTags } from "react-tag-input";
import { WrappedFieldProps } from "redux-form";
import { default as style } from "./index.css";

type CustomFieldProps = WrappedFieldProps & FormControlProps;

const renderError: ((arg1: string) => JSX.Element) = (msg: string): JSX.Element => (
  <HelpBlock id="validationError" className={style.validationError}>{msg}</HelpBlock>
);

const renderCharacterCount: ((text: string) => JSX.Element) = (text: string): JSX.Element => (
  <Badge pullRight={true} className={style.badge}>{text.length}</Badge>
);

type autocompleteFieldProps = CustomFieldProps & { suggestions: string[] };
export const autocompleteTextField: React.FC<autocompleteFieldProps> = (
  fieldProps: autocompleteFieldProps,
): JSX.Element => {
  const filteredSuggestions: string[] = _.isEmpty(fieldProps.input.value.trim())
    ? []
    : fieldProps.suggestions.filter((suggestion: string): boolean =>
      suggestion
        .toLowerCase()
        .includes(fieldProps.input.value.toLowerCase()));

  const renderSuggestion: ((suggestion: string) => JSX.Element) = (suggestion: string): JSX.Element => {
    const handleSuggestionClick: (() => void) = (): void => {
      fieldProps.input.onChange(suggestion);
    };

    return (
      <li onClick={handleSuggestionClick}><span>{suggestion}</span></li>
    );
  };

  const shouldRender: boolean = filteredSuggestions.length > 0 && filteredSuggestions[0] !== fieldProps.input.value;

  return (
    <div>
      <FormControl
        autoComplete="off"
        className={style.formControl}
        disabled={fieldProps.disabled}
        id={fieldProps.id}
        placeholder={fieldProps.placeholder}
        type={fieldProps.type}
        {...fieldProps.input}
      />
      {shouldRender ? <ul className={style.suggestionList}>{filteredSuggestions.map(renderSuggestion)}</ul> : undefined}
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );
};

export const textField: React.FC<CustomFieldProps> =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        className={style.formControl}
        id={fieldProps.id}
        type={fieldProps.type}
        placeholder={fieldProps.placeholder}
        min={fieldProps.min}
        max={fieldProps.max}
        value={fieldProps.input.value}
        onChange={fieldProps.input.onChange}
        onBlur={fieldProps.input.onBlur}
        disabled={fieldProps.disabled}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

type tagFieldProps = CustomFieldProps & { onDeletion(tag: string): void };
export const tagInputField: React.FC<tagFieldProps> =
  (fieldProps: tagFieldProps): JSX.Element => {
    const tagsEmpty: Tag[] = [];
    const { onDeletion } = fieldProps;
    const [tagsInput, setTagsInput] = React.useState(tagsEmpty);

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
      setTagsInput([...tagsInput, tag]);
      const newTag: string = tagToString([...tagsInput, tag]);
      fieldProps.input.onChange(newTag);
      fieldProps.input.value = newTag;
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
      <ReactTags
        allowDragDrop={false}
        classNames={styles}
        delimiters={Object.values(keyCodes)}
        handleDelete={handleDelete}
        handleAddition={handleAddition}
        handleInputBlur={handleInputBlur}
        inputFieldPosition="inline"
        name="tags"
        placeholder=""
        tags={tagsInput}
      />
    );
  };

export const phoneNumberField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => {
  const handlePhoneChange: PhoneInputProps["onChange"] = (value: string): void => {
    fieldProps.input.onChange(`+${value}`);
  };

  return (
    <PhoneInput
      country="co"
      masks={{ co: "(...) ... ...." }}
      inputClass={style.formControl}
      onChange={handlePhoneChange}
      value={fieldProps.input.value}
    />
  );
};

export const dropdownField: React.FC<CustomFieldProps> = (fieldProps: CustomFieldProps): JSX.Element => {
  const handleDropdownChange: React.FormEventHandler<FormControl> = (event: React.FormEvent<FormControl>): void => {
    fieldProps.input.onChange((event.target as HTMLInputElement).value);
  };

  return (
    <div>
      <FormControl
        className={style.formControl}
        componentClass="select"
        children={fieldProps.children}
        defaultValue={fieldProps.meta.initial}
        onChange={handleDropdownChange}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
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

export const textAreaField: React.FC<CustomFieldProps & { withCount?: boolean }> =
  (fieldProps: CustomFieldProps & { withCount?: boolean }): JSX.Element => (
    <div>
      <FormControl
        componentClass="textarea"
        {...fieldProps}
        {...fieldProps.input}
        className={`${style.formControl} ${fieldProps.className}`}
      />
      {fieldProps.withCount === true ? renderCharacterCount(fieldProps.input.value as string) : undefined}
      {(fieldProps.withCount === true && fieldProps.meta.error) ? <br /> : undefined}
      {fieldProps.meta.touched && fieldProps.meta.error ? renderError(fieldProps.meta.error as string) : undefined}
    </div>
  );

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
