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
  availableParameters: IAvailableParameter[];
  onSubmit: (parameters: IParameter[]) => void;
  placeholder?: string;
}

interface IFormValues {
  search: string;
}

export type { IAvailableParameter, IFormValues, IParameter, ISearchBarProps };
