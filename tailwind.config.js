/** @type {import('tailwindcss').Config} */
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
        heading: ['"Playfair Display"', "Georgia", "serif"],
        body: ["Lato", '"Open Sans"', "system-ui", "sans-serif"],
      },
      fontSize: {
        "hero": ["4.625rem", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
        "hero-mobile": ["2.5rem", { lineHeight: "1.15", letterSpacing: "-0.02em" }],
      },
    },
  },
  plugins: [],
};
