console.log("asdasdas")
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const payBtn = document.getElementById('pay-btn');
const statusText = document.getElementById('pay-status');

if (payBtn) {
    payBtn.addEventListener('click', async () => {
        const orderId = payBtn.dataset.orderId;
        const csrftoken = getCookie('csrftoken');

        payBtn.disabled = true;
        payBtn.textContent = 'Перенаправлення...';
        statusText.textContent = '';

        try {
            const response = await fetch(
                `/api/payments/liqpay/data/${orderId}/`,
                {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    credentials: 'include'
                }
            );

            if (!response.ok) {
                throw new Error('Помилка сервера');
            }

            const { data, signature } = await response.json();

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = 'https://www.liqpay.ua/api/3/checkout';

            form.innerHTML = `
                <input type="hidden" name="data" value="${data}">
                <input type="hidden" name="signature" value="${signature}">
            `;

            document.body.appendChild(form);
            form.submit();

        } catch (error) {
            payBtn.disabled = false;
            payBtn.textContent = 'Оплатити';
            statusText.textContent = 'Не вдалося почати оплату';
            console.error(error);
        }
    });
}
