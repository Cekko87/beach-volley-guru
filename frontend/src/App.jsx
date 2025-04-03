import React from "react";
import { useTranslation } from "react-i18next";

export default function App() {
  const { t } = useTranslation();
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>{t("welcome")}</h1>
      <p>{t("description")}</p>
    </div>
  );
}
