import React from 'react';
import { Style } from '../types';

interface StyleSelectorProps {
  style: Style;
  isSelected: boolean;
  onClick: () => void;
}

const StyleSelector: React.FC<StyleSelectorProps> = ({ style, isSelected, onClick }) => {
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
          src={style.previewImage}
          alt={style.name}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-2">
        <h4 className="text-sm font-medium text-gray-900 truncate">{style.name}</h4>
        <p className="text-xs text-gray-500 truncate">{style.description}</p>
      </div>
    </div>
  );
};

export default StyleSelector;