import React, { useState } from 'react';
import { Layers, ShoppingBag, Image, Palette, RefreshCw, Info } from 'lucide-react';
import ProductCard from './components/ProductCard';
import StyleSelector from './components/StyleSelector';
import { products } from './data/products';
import { styles } from './data/styles';

function App() {
  const [selectedProduct, setSelectedProduct] = useState(products[0]);
  const [selectedStyle, setSelectedStyle] = useState(styles[0]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleStyleTransfer = () => {
    setIsProcessing(true);
    // Simulate API call for style transfer
    setTimeout(() => {
      setIsProcessing(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Layers className="h-8 w-8 text-indigo-600" />
              <h1 className="ml-2 text-xl font-bold text-gray-900">StyleShift</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-500 hover:text-gray-700">
                <ShoppingBag className="h-6 w-6" />
              </button>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Sign In
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6">
            <div className="flex items-center mb-6">
              <Image className="h-6 w-6 text-indigo-600" />
              <h2 className="ml-2 text-lg font-medium text-gray-900">Style Transfer Demo</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Product Selection */}
              <div className="space-y-4">
                <h3 className="text-md font-medium text-gray-900 flex items-center">
                  <ShoppingBag className="h-5 w-5 mr-2 text-indigo-500" />
                  Select Product
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  {products.map((product) => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      isSelected={selectedProduct.id === product.id}
                      onClick={() => setSelectedProduct(product)}
                    />
                  ))}
                </div>
              </div>

              {/* Style Selection */}
              <div className="space-y-4">
                <h3 className="text-md font-medium text-gray-900 flex items-center">
                  <Palette className="h-5 w-5 mr-2 text-indigo-500" />
                  Select Style
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  {styles.map((style) => (
                    <StyleSelector
                      key={style.id}
                      style={style}
                      isSelected={selectedStyle.id === style.id}
                      onClick={() => setSelectedStyle(style)}
                    />
                  ))}
                </div>
                <button
                  onClick={handleStyleTransfer}
                  disabled={isProcessing}
                  className="w-full mt-4 bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300 flex items-center justify-center"
                >
                  {isProcessing ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    'Apply Style Transfer'
                  )}
                </button>
              </div>

              {/* Result Preview */}
              <div className="space-y-4">
                <h3 className="text-md font-medium text-gray-900 flex items-center">
                  <RefreshCw className="h-5 w-5 mr-2 text-indigo-500" />
                  Style Transfer Result
                </h3>
                <div className="border border-gray-200 rounded-lg overflow-hidden aspect-square">
                  <img
                    src={isProcessing ? '/processing.gif' : selectedProduct.styledImages[selectedStyle.id]}
                    alt={`${selectedProduct.name} in ${selectedStyle.name} style`}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex items-start space-x-2 text-sm text-gray-500">
                  <Info className="h-4 w-4 mt-0.5 flex-shrink-0" />
                  <p>
                    This demo simulates how CycleGAN technology transforms product images into different artistic styles.
                    In a production environment, this would connect to a FastAPI backend with Cassandra for style configuration storage.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Technology Explanation */}
        <div className="mt-8 bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">About This Technology</h2>
            <div className="prose max-w-none">
              <p>
                This application demonstrates how CycleGAN technology can enhance e-commerce experiences by allowing
                customers to visualize products in different artistic styles or environments.
              </p>
              <h3>Key Technologies:</h3>
              <ul>
                <li>
                  <strong>CycleGAN:</strong> An advanced generative adversarial network that enables unpaired
                  image-to-image translation, allowing products to be visualized in different styles without requiring
                  paired training data.
                </li>
                <li>
                  <strong>FastAPI:</strong> A high-performance Python web framework that would handle the backend
                  processing of style transfer requests in a production environment.
                </li>
                <li>
                  <strong>Apache Cassandra:</strong> A distributed NoSQL database used for storing style configurations,
                  user preferences, and processed image metadata, enabling fast retrieval of style transfer results.
                </li>
              </ul>
              <p>
                In a full implementation, this system would process images in real-time or near-real-time, allowing
                shoppers to see products in various contexts, increasing engagement and reducing return rates by setting
                appropriate expectations.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center">
              <Layers className="h-6 w-6 text-indigo-600" />
              <span className="ml-2 text-gray-900 font-medium">StyleShift</span>
            </div>
            <div className="mt-4 md:mt-0 text-sm text-gray-500">
              &copy; 2025 StyleShift. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;