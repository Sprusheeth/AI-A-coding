const dictionary = {
  en: {
    title: 'Multi-Language Website',
    subtitle: 'Switch language and keep your preference saved.',
    heading: 'Welcome to our learning portal',
    paragraph: 'This page updates text instantly using JavaScript translation objects.',
    button: 'Read More'
  },
  es: {
    title: 'Sitio Web Multilenguaje',
    subtitle: 'Cambia el idioma y guarda tu preferencia.',
    heading: 'Bienvenido a nuestro portal de aprendizaje',
    paragraph: 'Esta pagina actualiza el texto al instante usando objetos de traduccion en JavaScript.',
    button: 'Leer Mas'
  },
  ar: {
    title: 'موقع متعدد اللغات',
    subtitle: 'قم بتبديل اللغة مع حفظ اختيارك.',
    heading: 'مرحبا بك في بوابة التعلم',
    paragraph: 'تقوم هذه الصفحة بتحديث النص فورا باستخدام كائنات الترجمة في جافاسكريبت.',
    button: 'اقرأ المزيد'
  }
};

const LANG_KEY = 'lab14_language';
const selector = document.getElementById('languageSelect');

function applyLanguage(lang) {
  const content = dictionary[lang] || dictionary.en;

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.dataset.i18n;
    if (content[key]) {
      element.textContent = content[key];
    }
  });

  // Arabic requires right-to-left direction for correct reading flow.
  document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
  document.documentElement.setAttribute('lang', lang);

  localStorage.setItem(LANG_KEY, lang);
}

selector.addEventListener('change', (event) => {
  applyLanguage(event.target.value);
});

const saved = localStorage.getItem(LANG_KEY) || 'en';
selector.value = saved;
applyLanguage(saved);
