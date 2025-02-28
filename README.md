# StyleShift: Style Transfer Application for E-Commerce

StyleShift is an advanced e-commerce application that uses CycleGAN technology to transform product images into different artistic styles. This allows customers to visualize products in various contexts, enhancing the online shopping experience and potentially reducing return rates.

![StyleShift Demo](https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80)

## 🚀 Features

- **Interactive Product Visualization**: Select from a variety of products and see them rendered in different artistic styles
- **Real-time Style Transfer**: Powered by CycleGAN neural networks for high-quality image transformations
- **Multiple Style Options**: Choose from various artistic styles including Monochrome, Vintage, Nature, and Neon
- **Responsive Design**: Fully responsive UI that works on desktop and mobile devices

## 🛠️ Technology Stack

### Frontend
- **React**: For building the user interface
- **TypeScript**: For type-safe code
- **Tailwind CSS**: For styling
- **Vite**: For fast development and building

### Backend
- **FastAPI**: High-performance Python web framework
- **PyTorch**: Deep learning framework for implementing CycleGAN
- **Uvicorn**: ASGI server for running the FastAPI application

### Data Storage
- **Apache Cassandra**: Distributed NoSQL database for storing style configurations and processed image metadata
  - In the demo version, an in-memory database is used for simplicity

## 🧠 CycleGAN Architecture

The application uses CycleGAN (Cycle-Consistent Generative Adversarial Networks) for unpaired image-to-image translation. This allows for style transfer without requiring paired training data.

Key components:
- **Generator Networks**: Two generator networks (G_A and G_B) that learn to transform images from domain A to domain B and vice versa
- **Discriminator Networks**: Two discriminator networks that learn to distinguish between real and generated images
- **Cycle Consistency Loss**: Ensures that if we translate an image to another domain and back, we should get the original image

## 🏗️ Project Structure

```
styleshift/
├── backend/                  # Backend code
│   ├── app.py                # FastAPI application
│   ├── models/               # PyTorch model definitions
│   │   └── cycle_gan_model.py # CycleGAN implementation
│   ├── uploads/              # Directory for uploaded images
│   ├── results/              # Directory for processed images
│   └── requirements.txt      # Python dependencies
├── public/                   # Static assets
├── src/                      # Frontend code
│   ├── components/           # React components
│   │   ├── ProductCard.tsx   # Product selection card
│   │   └── StyleSelector.tsx # Style selection card
│   ├── data/                 # Data files
│   │   ├── products.ts       # Product information
│   │   └── styles.ts         # Style information
│   ├── types/                # TypeScript type definitions
│   ├── App.tsx               # Main application component
│   └── main.tsx              # Application entry point
├── package.json              # Node.js dependencies
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rukkya/styleshift.git
   cd styleshift
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Start the development servers:

   Frontend:
   ```bash
   npm run dev
   ```

   Backend:
   ```bash
   npm run backend
   ```

5. Open your browser and navigate to `http://localhost:5173`

## 🔄 API Endpoints

- `GET /api/styles`: Get all available styles
- `POST /api/transfer`: Apply style transfer to a product image
- `GET /api/health`: Check API health status

## 🧪 How It Works

1. **Select a Product**: Choose from available products in the catalog
2. **Select a Style**: Choose an artistic style to apply
3. **Apply Style Transfer**: Click the "Apply Style Transfer" button
4. **View Result**: The system processes the image using CycleGAN and displays the result

In a production environment:
1. The frontend sends a request to the FastAPI backend
2. The backend loads the appropriate CycleGAN model from storage
3. The model processes the product image to apply the selected style
4. The result is stored in Cassandra for fast retrieval
5. The transformed image URL is returned to the frontend for display

## 🔍 Technical Details

### CycleGAN Implementation

The CycleGAN model consists of:
- **ResNet Generator**: Uses 9 ResNet blocks for high-quality image transformation
- **PatchGAN Discriminator**: Classifies whether image patches are real or fake
- **Loss Functions**: Adversarial loss, cycle consistency loss, and identity loss

### Cassandra Schema (Production)

```cql
CREATE TABLE styles (
    id text PRIMARY KEY,
    name text,
    description text,
    model_path text
);

CREATE TABLE product_styles (
    id uuid PRIMARY KEY,
    product_id text,
    style_id text,
    image_url text,
    created_at timestamp
);
```

## 📈 Future Improvements

- **User Accounts**: Allow users to save favorite styled products
- **More Styles**: Add additional artistic styles and environments
- **Custom Style Upload**: Allow users to upload their own style reference images
- **Batch Processing**: Enable styling multiple products at once
- **Mobile App**: Develop native mobile applications for iOS and Android

## 🙏 Acknowledgements

- [CycleGAN Paper](https://arxiv.org/pdf/1703.10593.pdf) - Original research paper on CycleGAN
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Apache Cassandra](https://cassandra.apache.org/) - Distributed NoSQL database
