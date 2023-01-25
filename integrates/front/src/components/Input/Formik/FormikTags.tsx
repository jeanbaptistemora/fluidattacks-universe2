import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { Button } from "components/Button";
import { Tag } from "components/Tag";

type IInputTagsProps = IInputBase<HTMLInputElement>;

type TInputTagsProps = IInputTagsProps & TFieldProps;

const FormikTags: React.FC<TInputTagsProps> = ({
  disabled,
  field: { name, onBlur, onChange, value },
  form,
  id,
  label,
  onFocus,
  required,
  tooltip,
  variant = "solid",
}): JSX.Element => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      setInputValue(event.target.value);
    },
    []
  );

  const tags = value.split(",");

  const setTags = useCallback(
    (values: string[]): void => {
      const changeEvent = new Event("change");
      // eslint-disable-next-line fp/no-mutating-methods
      Object.defineProperty(changeEvent, "target", {
        value: { name, value: values.join(",") },
      });

      onChange(changeEvent);
    },
    [name, onChange]
  );

  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLInputElement>): void => {
      const trimmedValue = inputValue.trim();

      if (
        ["Enter", " ", ","].includes(event.key) &&
        trimmedValue.length &&
        !tags.includes(trimmedValue)
      ) {
        event.preventDefault();

        setTags([...tags, trimmedValue]);
        setInputValue("");
      } else if (
        event.key === "Backspace" &&
        !trimmedValue.length &&
        tags.length
      ) {
        event.preventDefault();
        setTags(tags.slice(0, -1));
      }
    },
    [inputValue, setTags, tags]
  );

  const removeTag = useCallback(
    (tag: string): VoidFunction => {
      return (): void => {
        setTags(tags.filter((currentValue): boolean => currentValue !== tag));
      };
    },
    [setTags, tags]
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={label}
      name={name}
      required={required}
      tooltip={tooltip}
      variant={variant}
    >
      {tags.map(
        (tag): JSX.Element => (
          <Tag key={tag} variant={"gray"}>
            {tag}&nbsp;
            <Button onClick={removeTag(tag)} size={"text"}>
              <FontAwesomeIcon icon={faClose} />
            </Button>
          </Tag>
        )
      )}
      <StyledInput
        aria-label={name}
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        name={name}
        onBlur={onBlur}
        onChange={handleInputChange}
        onFocus={onFocus}
        onKeyDown={handleKeyDown}
        type={"text"}
        value={inputValue}
      />
    </InputBase>
  );
};

export type { IInputTagsProps };
export { FormikTags };
