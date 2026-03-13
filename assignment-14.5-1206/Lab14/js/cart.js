const products = [
  { id: 1, name: 'Wireless Mouse', price: 25, image: 'https://picsum.photos/seed/mouse/400/300' },
  { id: 2, name: 'Mechanical Keyboard', price: 80, image: 'https://picsum.photos/seed/keyboard/400/300' },
  { id: 3, name: 'USB-C Hub', price: 45, image: 'https://picsum.photos/seed/hub/400/300' },
  { id: 4, name: 'Noise-Cancel Headset', price: 120, image: 'https://picsum.photos/seed/headset/400/300' },
  { id: 5, name: '4K Monitor Stand', price: 60, image: 'https://picsum.photos/seed/stand/400/300' }
];

const CART_KEY = 'lab14_cart';
let cart = loadCart();

const productsContainer = document.getElementById('products');
const cartContainer = document.getElementById('cartItems');
const totalPriceElement = document.getElementById('totalPrice');

function loadCart() {
  const saved = localStorage.getItem(CART_KEY);
  return saved ? JSON.parse(saved) : {};
}

function saveCart() {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function addToCart(productId) {
  cart[productId] = (cart[productId] || 0) + 1;
  saveCart();
  renderCart();
}

function updateQuantity(productId, delta) {
  const next = (cart[productId] || 0) + delta;
  if (next <= 0) {
    delete cart[productId];
  } else {
    cart[productId] = next;
  }
  saveCart();
  renderCart();
}

function removeItem(productId) {
  delete cart[productId];
  saveCart();
  renderCart();
}

function renderProducts() {
  productsContainer.innerHTML = products
    .map(
      (product) => `
      <article class="product-card">
        <img src="${product.image}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p>$${product.price.toFixed(2)}</p>
        <button class="btn btn-primary" data-add="${product.id}">Add to cart</button>
      </article>
    `
    )
    .join('');

  productsContainer.querySelectorAll('[data-add]').forEach((button) => {
    button.addEventListener('click', () => addToCart(button.dataset.add));
  });
}

function renderCart() {
  const entries = Object.entries(cart);
  if (!entries.length) {
    cartContainer.innerHTML = '<p>Your cart is empty.</p>';
    totalPriceElement.textContent = '$0.00';
    return;
  }

  let total = 0;
  cartContainer.innerHTML = entries
    .map(([id, quantity]) => {
      const product = products.find((item) => item.id === Number(id));
      const itemTotal = product.price * quantity;
      total += itemTotal;

      return `
        <article class="cart-item">
          <strong>${product.name}</strong>
          <p>$${product.price.toFixed(2)} x ${quantity} = $${itemTotal.toFixed(2)}</p>
          <div class="qty-row">
            <button class="btn btn-primary" data-delta="-1" data-id="${id}" aria-label="Decrease quantity">-</button>
            <button class="btn btn-primary" data-delta="1" data-id="${id}" aria-label="Increase quantity">+</button>
            <button class="btn btn-danger" data-remove="${id}">Remove</button>
          </div>
        </article>
      `;
    })
    .join('');

  totalPriceElement.textContent = `$${total.toFixed(2)}`;

  cartContainer.querySelectorAll('[data-delta]').forEach((button) => {
    button.addEventListener('click', () => updateQuantity(button.dataset.id, Number(button.dataset.delta)));
  });

  cartContainer.querySelectorAll('[data-remove]').forEach((button) => {
    button.addEventListener('click', () => removeItem(button.dataset.remove));
  });
}

renderProducts();
renderCart();
