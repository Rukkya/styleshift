export interface Product {
  id: string;
  name: string;
  category: string;
  image: string;
  styledImages: Record<string, string>;
}

export interface Style {
  id: string;
  name: string;
  description: string;
  previewImage: string;
}