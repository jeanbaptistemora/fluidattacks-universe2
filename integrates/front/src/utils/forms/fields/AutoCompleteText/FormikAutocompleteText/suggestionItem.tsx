import React, { useCallback } from "react";

interface ISuggestionItemProps {
  onChange: (value: string) => void;
  value: string;
}

export const SuggestionItem: React.FC<ISuggestionItemProps> = ({
  value,
  onChange,
}: ISuggestionItemProps): JSX.Element => {
  const handleClick = useCallback((): void => {
    onChange(value);
  }, [onChange, value]);

  return (
    <button onClick={handleClick}>
      <li>{value}</li>
    </button>
  );
};
