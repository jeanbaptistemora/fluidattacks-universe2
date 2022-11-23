interface IAvailableParameter {
  name: string;
  title: string;
  unique: boolean;
  options: string[];
}

interface IParameter extends IAvailableParameter {
  value: string;
}

interface ISearchBarProps {
  onSubmit: (search: string) => void;
  placeholder?: string;
}

interface IFormValues {
  search: string;
}

export type { IAvailableParameter, IFormValues, IParameter, ISearchBarProps };
