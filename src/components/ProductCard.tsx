import React from 'react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  isSelected: boolean;
  onClick: () => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, isSelected, onClick }) => {
  return (
    <div
      className={`border rounded-lg overflow-hidden cursor-pointer transition-all duration-200 ${
        isSelected
          ? 'border-indigo-500 ring-2 ring-indigo-200'
          : 'border-gray-200 hover:border-indigo-200'
      }`}
      onClick={onClick}
    >
      <div className="aspect-square bg-gray-100">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-2">
        <h4 className="text-sm font-medium text-gray-900 truncate">{product.name}</h4>
        <p className="text-xs text-gray-500 truncate">{product.category}</p>
      </div>
    </div>
  );
};

export default ProductCard;