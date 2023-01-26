import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import styled from "styled-components";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { StyledInput } from "../styles";
import { createEvent } from "../utils";
import { Button } from "components/Button";
import { Tag } from "components/Tag";

interface IInputTagsProps extends IInputBase<HTMLInputElement> {
  onRemove?: (tag: string) => void;
}

type TInputTagsProps = IInputTagsProps & TFieldProps;

const TagInput = styled(StyledInput)`
  flex: 1;
`;

const FormikTags: React.FC<Readonly<TInputTagsProps>> = ({
  disabled = false,
  field: { name, onBlur, onChange, value },
  form,
  id,
  label,
  onFocus,
  onRemove,
  placeholder,
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

  const tags = value.split(",").filter(Boolean);

  const setTags = useCallback(
    (values: string[]): void => {
      const changeEvent = createEvent("change", name, values.join(","));

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
        onRemove?.(tags[tags.length - 1]);
        setTags(tags.slice(0, -1));
      }
    },
    [inputValue, onRemove, setTags, tags]
  );

  const removeTag = useCallback(
    (tag: string): VoidFunction => {
      return (): void => {
        onRemove?.(tag);
        setTags(tags.filter((currentValue): boolean => currentValue !== tag));
      };
    },
    [onRemove, setTags, tags]
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
      <div className={"flex flex-wrap w-100"}>
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
        <TagInput
          aria-label={name}
          autoComplete={"off"}
          disabled={disabled}
          id={id}
          name={name}
          onBlur={onBlur}
          onChange={handleInputChange}
          onFocus={onFocus}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          type={"text"}
          value={inputValue}
        />
      </div>
    </InputBase>
  );
};

export type { IInputTagsProps };
export { FormikTags };
