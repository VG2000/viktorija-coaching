/** @type {import('tailwindcss').Config} */

/*
 * FONT THEME — Change fonts in ONE place
 * =======================================
 * 1. Update the font names below
 * 2. Update the Google Fonts <link> in viktorijacoaching/templates/base.html
 * 3. Run: npx tailwindcss@3 -i ... -o ...
 *
 * Current theme:
 *   Headings (h1-h4, logo): Bodoni Moda (high-contrast serif)
 *   Body (paragraphs, nav, buttons): Poppins (geometric sans-serif)
 */

module.exports = {
  content: [
    "./viktorijacoaching/templates/**/*.html",
    "./home/templates/**/*.html",
    "./pages/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#051C46",
          light: "#0A2D6E",
        },
        teal: {
          DEFAULT: "#0ABAB5",
          light: "#E0F5F4",
          dark: "#089E9A",
        },
        cream: "#FAF8F5",
        gold: {
          DEFAULT: "#B8860B",
          light: "#CCB57F",
        },
        "warm-tan": "#C4A484",
        blush: "#F5E6E6",
      },
      fontFamily: {
        heading: ['"Bodoni Moda"', "Didot", "Georgia", "serif"],
        body: ["Poppins", "system-ui", "sans-serif"],
      },
      fontSize: {
        "hero": ["4.625rem", { lineHeight: "1.05", letterSpacing: "-0.02em" }],
        "hero-mobile": ["2.5rem", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
      },
    },
  },
  plugins: [],
};
