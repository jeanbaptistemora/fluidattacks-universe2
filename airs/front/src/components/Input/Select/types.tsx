interface ISelectProps {
  label?: string;
  onChange: (selectedOption: string) => void;
  options: string[];
}

export type { ISelectProps };
