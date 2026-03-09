// Якщо функція в іншому файлі і він підключений раніше, вона буде доступна глобально.
// Якщо ні — можна просто залишити її тут:
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

document.addEventListener('DOMContentLoaded', function () {
    const checkoutForm = document.getElementById('checkoutForm');
    const btn = document.getElementById('submitBtn');
    const paymentCards = document.querySelectorAll('.payment-card');

    // Перемикання стилів та тексту кнопки
    paymentCards.forEach(card => {
        card.addEventListener('click', function() {
            paymentCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            const radio = this.querySelector('input');
            radio.checked = true;

            if (radio.value === 'online') {
                btn.innerHTML = '<span>Оплатити зараз</span> <i class="fa-solid fa-arrow-right"></i>';
            } else {
                btn.innerHTML = '<span>Підтвердити замовлення</span> <i class="fa-solid fa-check"></i>';
            }
        });
    });

    checkoutForm.addEventListener('submit', async function (e) {
        const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;

        if (paymentMethod === 'online') {
            e.preventDefault();
            
            const formData = new FormData(checkoutForm);
            const csrftoken = getCookie('csrftoken'); // Отримуємо токен

            try {
                btn.disabled = true;
                btn.innerHTML = '<span>Обробка...</span> <i class="fa-solid fa-spinner fa-spin"></i>';

                // 1. Створюємо замовлення
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken // Додаємо токен тут!
                    }
                });

                const result = await response.json();

                if (result.success && result.order_id) {
                    // 2. Запит до твого API за даними LiqPay
                    // Переконайся, що шлях відповідає urls.py
                    const lpResponse = await fetch(`/payment/liqpay/data/${result.order_id}/`);
                    const lpData = await lpResponse.json();

                    // 3. Створення та сабміт форми LiqPay
                    const liqpayForm = document.createElement('form');
                    liqpayForm.method = 'POST';
                    liqpayForm.action = 'https://www.liqpay.ua/api/3/checkout';
                    liqpayForm.acceptCharset = 'utf-8';

                    // Додаємо data
                    const inputData = document.createElement('input');
                    inputData.type = 'hidden';
                    inputData.name = 'data';
                    inputData.value = lpData.data;
                    liqpayForm.appendChild(inputData);

                    // Додаємо signature
                    const inputSig = document.createElement('input');
                    inputSig.type = 'hidden';
                    inputSig.name = 'signature';
                    inputSig.value = lpData.signature;
                    liqpayForm.appendChild(inputSig);

                    document.body.appendChild(liqpayForm);
                    liqpayForm.submit();
                } else {
                    alert('Помилка при створенні замовлення. Перевірте дані.');
                    btn.disabled = false;
                    btn.innerHTML = '<span>Оплатити зараз</span> <i class="fa-solid fa-arrow-right"></i>';
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Сталася помилка зв’язку з сервером.');
                btn.disabled = false;
            }
        }
    });
});