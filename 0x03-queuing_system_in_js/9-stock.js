import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Data
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Helper function
function getItemById(id) {
  return listProducts.find((product) => product.id === id);
}

// Create Redis client and promisify methods
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve stock by ID
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock by ID
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0;
}

// Create Express app
const app = express();
const PORT = 1245;

// Routes
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currentQuantity = product.stock - await getCurrentReservedStockById(itemId);

  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const currentReserved = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - currentReserved;

  if (currentQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, currentReserved + 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
