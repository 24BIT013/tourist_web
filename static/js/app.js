document.addEventListener('DOMContentLoaded', () => {
    const translations = {
        en: {
            'nav.home': 'Home', 'nav.packages': 'Packages', 'nav.gallery': 'Gallery',
            'nav.book': 'Book a trip', 'nav.contact': 'Contact', 'nav.plan': 'Plan a trip',
            'whatsapp.chat': 'WhatsApp chat', 'whatsapp.help': 'Need help planning a trip? Chat with us on WhatsApp and we will reply quickly.',
            'whatsapp.start': 'Start chat', 'home.eyebrow': 'Explore Zanji adventures',
            'home.title': 'Find your next unforgettable Zanji adventure.',
            'home.copy': 'Discover Zanzibar, where every wave tells a story and every step leads to an authentic adventure: beach escapes, spice routes, and seamless transfers.',
            'home.explore': 'Explore tours', 'home.how': 'How it works',
            'home.tours_intro': "Our tours are thoughtfully planned for every kind of traveller, combining Zanzibar's beaches, culture, nature, and local flavours into relaxed, memorable days.",
        },
        sw: {
            'nav.home': 'Nyumbani', 'nav.packages': 'Ziara', 'nav.gallery': 'Picha',
            'nav.book': 'Weka nafasi', 'nav.contact': 'Wasiliana nasi', 'nav.plan': 'Panga safari',
            'whatsapp.chat': 'Ongea nasi WhatsApp', 'whatsapp.help': 'Unahitaji msaada kupanga safari? Ongea nasi kupitia WhatsApp na tutajibu haraka.',
            'whatsapp.start': 'Anza mazungumzo', 'home.eyebrow': 'Gundua dunia kwa namna tofauti',
            'home.title': 'Pata safari yako ijayo isiyosahaulika.',
            'home.copy': 'Gundua safari zilizopangwa, hadithi za wenyeji, malazi mazuri na nyakati zinazobadilisha jinsi unavyoiona dunia.',
            'home.explore': 'Chunguza ziara', 'home.how': 'Jinsi inavyofanya kazi',
            'home.tours_intro': 'Ziara zetu hupangwa kwa uangalifu kwa kila aina ya msafiri, zikichanganya fukwe, utamaduni, mazingira na ladha za Zanzibar kwa siku za kukumbukwa.',
        },
        es: {
            'nav.home': 'Inicio', 'nav.packages': 'Paquetes', 'nav.gallery': 'Galería', 'nav.book': 'Reservar un viaje', 'nav.contact': 'Contacto', 'nav.plan': 'Planifica un viaje', 'whatsapp.chat': 'Chat de WhatsApp', 'whatsapp.help': '¿Necesitas ayuda para planificar un viaje? Escríbenos por WhatsApp y responderemos pronto.', 'whatsapp.start': 'Iniciar chat',
            'home.eyebrow': 'Explora las aventuras de Zanji', 'home.title': 'Encuentra tu próxima aventura inolvidable en Zanji.', 'home.copy': 'Descubre Zanzíbar, donde cada ola cuenta una historia y cada paso conduce a una aventura auténtica: escapadas de playa, rutas de especias y traslados sin complicaciones.', 'home.explore': 'Explorar tours', 'home.how': 'Cómo funciona', 'home.tours_intro': 'Nuestros tours están cuidadosamente diseñados para cada tipo de viajero, combinando las playas, cultura, naturaleza y sabores locales de Zanzíbar en días relajados e inolvidables.',
        },
        fr: {
            'nav.home': 'Accueil', 'nav.packages': 'Circuits', 'nav.gallery': 'Galerie', 'nav.book': 'Réserver un voyage', 'nav.contact': 'Contact', 'nav.plan': 'Planifier un voyage', 'whatsapp.chat': 'Discussion WhatsApp', 'whatsapp.help': 'Besoin d’aide pour préparer votre voyage ? Écrivez-nous sur WhatsApp, nous répondrons rapidement.', 'whatsapp.start': 'Démarrer la discussion',
            'home.eyebrow': 'Explorez les aventures Zanji', 'home.title': 'Trouvez votre prochaine aventure inoubliable à Zanji.', 'home.copy': 'Découvrez Zanzibar, où chaque vague raconte une histoire et chaque pas mène à une aventure authentique : plages, routes des épices et transferts fluides.', 'home.explore': 'Explorer les circuits', 'home.how': 'Comment ça marche', 'home.tours_intro': 'Nos circuits sont conçus avec soin pour tous les voyageurs et réunissent les plages, la culture, la nature et les saveurs locales de Zanzibar dans des journées mémorables.',
        },
        de: {
            'nav.home': 'Startseite', 'nav.packages': 'Pakete', 'nav.gallery': 'Galerie', 'nav.book': 'Reise buchen', 'nav.contact': 'Kontakt', 'nav.plan': 'Reise planen', 'whatsapp.chat': 'WhatsApp-Chat', 'whatsapp.help': 'Brauchen Sie Hilfe bei der Reiseplanung? Schreiben Sie uns auf WhatsApp – wir antworten schnell.', 'whatsapp.start': 'Chat starten',
            'home.eyebrow': 'Entdecken Sie Zanji-Abenteuer', 'home.title': 'Finden Sie Ihr nächstes unvergessliches Zanji-Abenteuer.', 'home.copy': 'Entdecken Sie Sansibar, wo jede Welle eine Geschichte erzählt und jeder Schritt zu einem authentischen Abenteuer führt: Strandauszeiten, Gewürzrouten und reibungslose Transfers.', 'home.explore': 'Touren entdecken', 'home.how': 'So funktioniert es', 'home.tours_intro': 'Unsere Touren sind sorgfältig für jede Art von Reisenden geplant und verbinden Sansibars Strände, Kultur, Natur und lokale Aromen zu entspannten, unvergesslichen Tagen.',
        },
        it: {
            'nav.home': 'Home', 'nav.packages': 'Pacchetti', 'nav.gallery': 'Galleria', 'nav.book': 'Prenota un viaggio', 'nav.contact': 'Contatti', 'nav.plan': 'Pianifica un viaggio', 'whatsapp.chat': 'Chat WhatsApp', 'whatsapp.help': 'Hai bisogno di aiuto per organizzare un viaggio? Scrivici su WhatsApp e risponderemo presto.', 'whatsapp.start': 'Avvia chat',
            'home.eyebrow': 'Esplora le avventure Zanji', 'home.title': 'Trova la tua prossima indimenticabile avventura Zanji.', 'home.copy': 'Scopri Zanzibar, dove ogni onda racconta una storia e ogni passo conduce a un’avventura autentica: fughe al mare, percorsi delle spezie e trasferimenti senza pensieri.', 'home.explore': 'Esplora i tour', 'home.how': 'Come funziona', 'home.tours_intro': 'I nostri tour sono pensati con cura per ogni tipo di viaggiatore e uniscono spiagge, cultura, natura e sapori locali di Zanzibar in giornate rilassate e memorabili.',
        },
        pl: {
            'nav.home': 'Strona główna', 'nav.packages': 'Pakiety', 'nav.gallery': 'Galeria', 'nav.book': 'Zarezerwuj podróż', 'nav.contact': 'Kontakt', 'nav.plan': 'Zaplanuj podróż', 'whatsapp.chat': 'Czat WhatsApp', 'whatsapp.help': 'Potrzebujesz pomocy w planowaniu podróży? Napisz do nas przez WhatsApp — odpowiemy szybko.', 'whatsapp.start': 'Rozpocznij czat',
            'home.eyebrow': 'Odkrywaj przygody Zanji', 'home.title': 'Znajdź swoją następną niezapomnianą przygodę Zanji.', 'home.copy': 'Odkryj Zanzibar, gdzie każda fala opowiada historię, a każdy krok prowadzi do prawdziwej przygody: plaż, tras przypraw i wygodnych transferów.', 'home.explore': 'Odkryj wycieczki', 'home.how': 'Jak to działa', 'home.tours_intro': 'Nasze wycieczki są starannie przygotowane dla każdego podróżnika i łączą plaże, kulturę, naturę oraz lokalne smaki Zanzibaru w spokojne, niezapomniane dni.',
        },
        pt: {
            'nav.home': 'Início', 'nav.packages': 'Pacotes', 'nav.gallery': 'Galeria', 'nav.book': 'Reservar uma viagem', 'nav.contact': 'Contacto', 'nav.plan': 'Planear uma viagem', 'whatsapp.chat': 'Chat no WhatsApp', 'whatsapp.help': 'Precisa de ajuda para planear uma viagem? Fale connosco no WhatsApp e responderemos rapidamente.', 'whatsapp.start': 'Iniciar conversa',
            'home.eyebrow': 'Explore as aventuras Zanji', 'home.title': 'Encontre a sua próxima aventura inesquecível em Zanji.', 'home.copy': 'Descubra Zanzibar, onde cada onda conta uma história e cada passo leva a uma aventura autêntica: escapadas de praia, rotas das especiarias e transferes tranquilos.', 'home.explore': 'Explorar tours', 'home.how': 'Como funciona', 'home.tours_intro': 'Os nossos tours são cuidadosamente planeados para todos os viajantes, combinando as praias, cultura, natureza e sabores locais de Zanzibar em dias relaxados e memoráveis.',
        },
    };

    const applyLanguage = (language) => {
        const dictionary = translations[language] || translations.en;
        document.documentElement.lang = language;
        document.querySelectorAll('[data-i18n]').forEach((element) => {
            const translation = dictionary[element.dataset.i18n];
            if (translation) element.textContent = translation;
        });
        const languageSelect = document.querySelector('[data-language-select]');
        if (languageSelect) languageSelect.value = language;
        localStorage.setItem('zanji-language', language);
    };

    document.querySelector('[data-language-select]')?.addEventListener('change', (event) => applyLanguage(event.target.value));
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
