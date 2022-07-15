/* eslint-disable react/require-default-props */
/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-autofocus */
import { faMinus, faPlus } from "@fortawesome/free-solid-svg-icons";
import _ from "lodash";
import React, { useEffect, useRef, useState } from "react";

import {
  Col50,
  Row,
  StyledFontAwesomeIcon,
  StyledInput,
  StyledInputContainer,
  VerticalLine,
} from "./styles";

import { Tooltip } from "components/Tooltip";

interface INumberInputProps {
  defaultValue: number;
  max: number;
  min: number;
  onEnter: (newValue: number | undefined) => void;
  tooltipMessage?: string;
}

const NumberInput: React.FC<INumberInputProps> = ({
  defaultValue,
  max,
  min,
  onEnter,
  tooltipMessage,
}): JSX.Element => {
  const [value, setValue] = useState(_.toString(defaultValue));
  const [spin, setSpin] = useState(false);
  const inputReference: React.MutableRefObject<HTMLInputElement | null> =
    useRef(null);

  const getCurrentNumber = (): number => _.toNumber(value);

  function handleOnInputChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    const newValue = _.toNumber(event.target.value);
    if (newValue >= min && newValue <= max) {
      setValue(event.target.value);
    }
    event.stopPropagation();
  }

  function handleOnInputContainerBlur(
    event: React.FocusEvent<HTMLInputElement>
  ): void {
    if (!event.currentTarget.contains(event.relatedTarget)) {
      setValue(_.toString(defaultValue));
    }
    event.stopPropagation();
  }

  function handleOnInputFocus(event: React.FocusEvent<HTMLInputElement>): void {
    event.stopPropagation();
  }

  function handleOnInputKeyUp(
    event: React.KeyboardEvent<HTMLInputElement>
  ): void {
    event.stopPropagation();
    if (event.key === "Enter" && !_.isEmpty(event.currentTarget.value)) {
      const newValue = _.isEmpty(event.currentTarget.value)
        ? undefined
        : _.toNumber(event.currentTarget.value);
      onEnter(newValue);
    }
  }

  function handleInputKeyDown(
    event: React.KeyboardEvent<HTMLInputElement>
  ): void {
    if (
      event.key.length > 1 ||
      /\d/u.test(event.key) ||
      event.key === "Control" ||
      event.key.toLocaleLowerCase() === "c"
    )
      return;
    event.preventDefault();
  }

  function handleOnMinusClick(event: React.MouseEvent<HTMLInputElement>): void {
    event.stopPropagation();
    const newNumber = getCurrentNumber() - 1;
    if (newNumber >= min && newNumber <= max) {
      setValue(_.toString(newNumber));
    }
    setSpin(true);
  }

  function handleOnPlusClick(event: React.MouseEvent<HTMLDivElement>): void {
    event.stopPropagation();
    const newNumber = getCurrentNumber() + 1;
    if (newNumber >= min && newNumber <= max) {
      setValue(_.toString(newNumber));
    }
    setSpin(true);
  }

  useEffect((): void => {
    if (inputReference.current !== null && spin) {
      inputReference.current.focus();
      setSpin(false);
    }
  }, [value, spin]);

  return (
    <StyledInputContainer onBlur={handleOnInputContainerBlur} tabIndex={-1}>
      <Tooltip id={"numberInputTooltip"} tip={tooltipMessage}>
        <Row>
          <Col50>
            <StyledInput
              max={max}
              min={min}
              onChange={handleOnInputChange}
              onFocus={handleOnInputFocus}
              onKeyDown={handleInputKeyDown}
              onKeyUp={handleOnInputKeyUp}
              ref={inputReference}
              step={"1"}
              type={"number"}
              value={value}
            />
          </Col50>
          <Col50>
            <Row>
              <Col50 onClick={handleOnMinusClick}>
                <StyledFontAwesomeIcon icon={faMinus} tabIndex={-1} />
              </Col50>
              <VerticalLine />
              <Col50 onClick={handleOnPlusClick}>
                <StyledFontAwesomeIcon icon={faPlus} tabIndex={-1} />
              </Col50>
            </Row>
          </Col50>
        </Row>
      </Tooltip>
    </StyledInputContainer>
  );
};

export type { INumberInputProps };
export { NumberInput };
