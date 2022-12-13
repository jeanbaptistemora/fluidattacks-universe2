interface IStyledInputProps {
  bgColor?: string;
  borderColor?: string;
}

interface IInputProps {
  label?: string;
  onChange: (value: string) => void;
  placeHolder?: string;
}

export type { IInputProps, IStyledInputProps };
