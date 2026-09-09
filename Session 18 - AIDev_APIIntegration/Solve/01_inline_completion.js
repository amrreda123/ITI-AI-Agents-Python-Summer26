function calculateTotalPrice(subtotal, taxRate = 0.08) {
  if (subtotal < 0) throw new Error("Subtotal must be positive");
  const tax = subtotal * taxRate;
  return Number((subtotal + tax).toFixed(2));
}

function truncateText(text, maxLength = 50) {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "...";
}

function debounce(func, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => func.apply(this, args), delay);
  };
}

console.log("Total Price ($100 with 8% tax):", calculateTotalPrice(100));
console.log("Truncated:", truncateText("AI-Assisted Development & LLM Integration Course in Python", 30));
