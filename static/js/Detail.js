function increment() {
    const quantityInput = document.getElementById("quantity");
    let current = parseInt(quantityInput.value);
    quantityInput.value = current + 1;
    updatePrice();
}

function decrement() {
    const quantityInput = document.getElementById("quantity");
    let current = parseInt(quantityInput.value);
    if (current > 1) {
        quantityInput.value = current - 1;
        updatePrice();
    }
}

function updatePrice() {
    let quantity = parseInt(document.getElementById('quantity').value);
    let weight = parseInt(document.getElementById('weight').value);
    let basePrice = parseFloat(document.getElementById('base-price').dataset.price);
    let totalPrice = (basePrice * weight / 1000) * quantity;
    document.getElementById('price-display').textContent = `₹${totalPrice.toFixed(2)}`;
}

window.onload = function () {
    updatePrice();
    document.getElementById('weight').addEventListener('change', updatePrice);
    document.getElementById('quantity').addEventListener('change', updatePrice); 
};
