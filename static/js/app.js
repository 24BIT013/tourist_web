document.addEventListener('DOMContentLoaded', () => {
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
