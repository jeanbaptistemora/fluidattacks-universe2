import type { IconProp } from "@fortawesome/fontawesome-svg-core";

interface IBenefits {
  id: number;
  data: string;
  icon: IconProp;
}

interface IQuotes {
  quote: string;
  reference: string;
}

export type { IBenefits, IQuotes };
