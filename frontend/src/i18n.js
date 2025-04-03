import i18n from "i18next";
import { initReactI18next } from "react-i18next";

i18n.use(initReactI18next).init({
  resources: {
    it: {
      translation: {
        welcome: "Benvenuto su Beach Volley Guru",
        description: "Analisi video automatica per il beach volley"
      }
    },
    en: {
      translation: {
        welcome: "Welcome to Beach Volley Guru",
        description: "Automatic video analysis for beach volleyball"
      }
    }
  },
  lng: "it",
  fallbackLng: "en",
  interpolation: {
    escapeValue: false
  }
});

export default i18n;
