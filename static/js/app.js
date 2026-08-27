document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.booking-form').forEach((form) => {
        const packageSelect = form.querySelector('[data-price-selector]');
        const travelersInput = form.querySelector('#id_travelers');
        const totalPrice = form.querySelector('[data-total-price]');
        const breakdown = form.querySelector('[data-price-breakdown]');

        if (!packageSelect || !travelersInput || !totalPrice || !breakdown) return;

        const updateTotal = () => {
            const selected = packageSelect.options[packageSelect.selectedIndex];
            const priceLabel = selected?.dataset.price;
            const travelers = Math.max(1, Number.parseInt(travelersInput.value, 10) || 1);
            const match = priceLabel?.match(/([€£$])?\s*([0-9][0-9,]*(?:\.\d{1,2})?)/);

            if (!match) {
                totalPrice.textContent = 'Select a package and number of travelers';
                breakdown.textContent = 'Prices are calculated per traveler.';
                return;
            }

            const amount = Number.parseFloat(match[2].replaceAll(',', '')) * travelers;
            const formatted = new Intl.NumberFormat('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2,
            }).format(amount);
            totalPrice.textContent = `${match[1] || ''}${formatted}`;
            breakdown.textContent = `${priceLabel} per traveler × ${travelers}`;
        };

        packageSelect.addEventListener('change', updateTotal);
        travelersInput.addEventListener('input', updateTotal);
        updateTotal();
    });

    const whatsappWidget = document.querySelector('[data-whatsapp-widget]');
    if (whatsappWidget) {
        const toggleButton = whatsappWidget.querySelector('.whatsapp-fab');
        const panel = whatsappWidget.querySelector('.whatsapp-panel');

        const setOpenState = (isOpen) => {
            whatsappWidget.classList.toggle('is-open', isOpen);
            toggleButton.setAttribute('aria-expanded', String(isOpen));
            panel.hidden = !isOpen;
        };

        setOpenState(false);

        toggleButton.addEventListener('click', () => {
            setOpenState(!whatsappWidget.classList.contains('is-open'));
        });

        document.addEventListener('click', (event) => {
            if (!whatsappWidget.contains(event.target)) {
                setOpenState(false);
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                setOpenState(false);
            }
        });
    }
});
