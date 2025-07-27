module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "plugin:prettier/recommended", // <-- adds prettier plugin & config
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: "module",
  },
  rules: {
    // allow single-word component names
    "vue/multi-word-component-names": "off",
    // any further custom ESLint rules…
  },
};
