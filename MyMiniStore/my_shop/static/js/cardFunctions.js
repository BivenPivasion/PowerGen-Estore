
// Денис
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Денис
function addToCart(event, btn) {
    event.preventDefault(); // Зупиняємо перехід по посиланню (якщо кнопка в <a>)
    
    const url = btn.getAttribute('data-url');
    const badge = document.getElementById('cart-count');

    // Блокуємо кнопку від повторних натискань до завершення запиту
    btn.style.pointerEvents = 'none';

    fetch(url, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': getCookie('csrftoken') 
        },
    })
    .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            // Оновлюємо кількість у кошику
            if (badge) badge.innerText = data.cart_total_items;

            // Фідбек на кнопці
            const originalText = btn.innerText;
            btn.innerText = 'ДОДАНО!';
            btn.style.background = '#2ecc71';

            setTimeout(() => { 
                btn.innerText = originalText; 
                btn.style.background = ''; 
                btn.style.pointerEvents = 'auto'; // Повертаємо можливість кліку
            }, 2000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.style.pointerEvents = 'auto';
        alert('Помилка при додаванні');
    });
}

// Денис
function changeQty(delta) {
    const input = document.querySelector('.qty-selector input');
    let newVal = parseInt(input.value) + delta;
    if (newVal >= parseInt(input.min) && newVal <= parseInt(input.max)) {
        input.value = newVal;
    }
}

// Денис
function addToCartWithQty(event, btn) {
    event.preventDefault();
    
    const url = btn.getAttribute('data-url');
    const productId = btn.getAttribute('data-product-id');
    const badge = document.getElementById('cart-count');
    const qtyInput = document.getElementById(`product-qty-${productId}`);
    const quantity = qtyInput ? qtyInput.value : 1;

    btn.style.pointerEvents = 'none';

    fetch(url, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
            // Замість {{ csrf_token }} використовуємо функцію:
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            'quantity': parseInt(quantity)
        })
    })
    .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            if (badge) badge.innerText = data.cart_total_items;
            const originalText = btn.innerText;
            btn.innerText = 'ДОДАНО!';
            btn.style.background = '#2ecc71';
            setTimeout(() => { 
                btn.innerText = originalText; 
                btn.style.background = ''; 
                btn.style.pointerEvents = 'auto'; 
            }, 2000);
        } else {
            alert(data.message); // Виведемо повідомлення про від'ємне число, якщо воно прийде
            btn.style.pointerEvents = 'auto';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.style.pointerEvents = 'auto';
        alert('Помилка при додаванні');
    });
}

// Денис
function updateCartItem(productId, action) {
    const url = action === 'plus' ? `/card/cart/add/${productId}/` : `/card/cart/minus/${productId}/`;

    console.log("Fetching URL:", url);
    
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // 1. Оновлюємо значок у хедері
            const badge = document.getElementById('cart-count');
            if (badge) badge.innerText = data.cart_total_items;

            const qtyElement = document.getElementById(`qty-${productId}`);
            const totalItemPriceElement = document.getElementById(`total-${productId}`);
            let currentQty = parseInt(qtyElement.innerText);
            
            // 2. Якщо кількість стала 0 або ми натиснули мінус на 1 шт
            if (action === 'minus' && currentQty <= 1) {
                const card = document.getElementById(`item-${productId}`);
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    card.remove();
                    // Якщо кошик став порожнім - показуємо пустий стан
                    if (data.cart_total_items === 0) {
                        location.reload(); 
                    }
                }, 300);
            } else {
                // 3. Оновлюємо цифру кількості
                qtyElement.innerText = action === 'plus' ? currentQty + 1 : currentQty - 1;
                
                // 4. Оновлюємо ціну конкретного рядка
                if (totalItemPriceElement) {
                    totalItemPriceElement.innerText = `$${data.item_total_price.toFixed(2)}`;
                }
            }

            // 5. Оновлюємо фінальні суми в блоці "Підсумок"
            const finalPriceElements = document.querySelectorAll('.final-price');
            const subtotalElements = document.querySelectorAll('.summary-line span:last-child');
            
            finalPriceElements.forEach(el => el.innerText = `$${data.total_price.toFixed(2)}`);
            // Оновлюємо перший рядок підсумку (Товари)
            if (subtotalElements[0]) {
                subtotalElements[0].innerText = `$${data.total_price.toFixed(2)}`;
            }
        }
    })
    .catch(err => console.error('Помилка:', err));
}