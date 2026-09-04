document.addEventListener('DOMContentLoaded', () => {
    const translations = {
        en: {
            'nav.home': 'Home', 'nav.packages': 'Packages', 'nav.gallery': 'Gallery',
            'nav.book': 'Book a trip', 'nav.contact': 'Contact', 'nav.plan': 'Plan a trip',
            'whatsapp.chat': 'WhatsApp chat', 'whatsapp.help': 'Need help planning a trip? Chat with us on WhatsApp and we will reply quickly.',
            'whatsapp.start': 'Start chat', 'home.eyebrow': 'Explore the world differently',
            'home.title': 'Find your next unforgettable adventure.',
            'home.copy': 'Discover curated journeys, local stories, beautiful stays, and moments that change the way you see the world.',
            'home.explore': 'Explore tours', 'home.how': 'How it works',
        },
        sw: {
            'nav.home': 'Nyumbani', 'nav.packages': 'Ziara', 'nav.gallery': 'Picha',
            'nav.book': 'Weka nafasi', 'nav.contact': 'Wasiliana nasi', 'nav.plan': 'Panga safari',
            'whatsapp.chat': 'Ongea nasi WhatsApp', 'whatsapp.help': 'Unahitaji msaada kupanga safari? Ongea nasi kupitia WhatsApp na tutajibu haraka.',
            'whatsapp.start': 'Anza mazungumzo', 'home.eyebrow': 'Gundua dunia kwa namna tofauti',
            'home.title': 'Pata safari yako ijayo isiyosahaulika.',
            'home.copy': 'Gundua safari zilizopangwa, hadithi za wenyeji, malazi mazuri na nyakati zinazobadilisha jinsi unavyoiona dunia.',
            'home.explore': 'Chunguza ziara', 'home.how': 'Jinsi inavyofanya kazi',
        },
    };

    const applyLanguage = (language) => {
        const dictionary = translations[language] || translations.en;
        document.documentElement.lang = language;
        document.querySelectorAll('[data-i18n]').forEach((element) => {
            const translation = dictionary[element.dataset.i18n];
            if (translation) element.textContent = translation;
        });
        document.querySelectorAll('[data-language]').forEach((button) => {
            const isActive = button.dataset.language === language;
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', String(isActive));
        });
        localStorage.setItem('zanji-language', language);
    };

    document.querySelectorAll('[data-language]').forEach((button) => {
        button.addEventListener('click', () => applyLanguage(button.dataset.language));
    });
    applyLanguage(localStorage.getItem('zanji-language') || 'en');

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

    document.querySelectorAll('[data-gallery-slider]').forEach((slider) => {
        const track = slider.querySelector('.gallery-track');
        const slides = [...slider.querySelectorAll('[data-gallery-slide]')];
        const previous = slider.querySelector('[data-gallery-previous]');
        const next = slider.querySelector('[data-gallery-next]');
        const dots = slider.querySelector('[data-gallery-dots]');
        if (!track || slides.length < 2 || !previous || !next || !dots) return;

        let currentIndex = 0;
        let timer;
        let touchStartX = 0;

        const dotButtons = slides.map((slide, index) => {
            const dot = document.createElement('button');
            dot.type = 'button';
            dot.className = 'gallery-dot';
            dot.setAttribute('aria-label', `Show photo ${index + 1}`);
            dot.addEventListener('click', () => showSlide(index));
            dots.append(dot);
            return dot;
        });

        const showSlide = (index) => {
            currentIndex = (index + slides.length) % slides.length;
            track.style.transform = `translateX(-${currentIndex * 100}%)`;
            slides.forEach((slide, slideIndex) => {
                slide.setAttribute('aria-hidden', String(slideIndex !== currentIndex));
            });
            dotButtons.forEach((dot, dotIndex) => {
                const isActive = dotIndex === currentIndex;
                dot.classList.toggle('is-active', isActive);
                dot.setAttribute('aria-current', String(isActive));
            });
        };

        const restartAutoplay = () => {
            window.clearInterval(timer);
            timer = window.setInterval(() => showSlide(currentIndex + 1), 5000);
        };

        previous.addEventListener('click', () => {
            showSlide(currentIndex - 1);
            restartAutoplay();
        });
        next.addEventListener('click', () => {
            showSlide(currentIndex + 1);
            restartAutoplay();
        });
        slider.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft') previous.click();
            if (event.key === 'ArrowRight') next.click();
        });
        slider.addEventListener('mouseenter', () => window.clearInterval(timer));
        slider.addEventListener('mouseleave', restartAutoplay);
        slider.addEventListener('touchstart', (event) => {
            touchStartX = event.changedTouches[0].screenX;
        }, { passive: true });
        slider.addEventListener('touchend', (event) => {
            const distance = event.changedTouches[0].screenX - touchStartX;
            if (Math.abs(distance) > 40) {
                showSlide(currentIndex + (distance < 0 ? 1 : -1));
                restartAutoplay();
            }
        }, { passive: true });

        showSlide(0);
        restartAutoplay();
    });
});
