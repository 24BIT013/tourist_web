document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.main-nav');
    if (nav) {
        nav.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                nav.querySelectorAll('a').forEach((item) => item.classList.toggle('active', item === link));
            });
        });
    }

    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const button = bookingForm.querySelector('button');
            if (button) {
                button.textContent = 'Request sent';
                button.disabled = true;
            }
        });
    }
});
