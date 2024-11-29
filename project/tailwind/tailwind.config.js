/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "../**/forms.py"],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
    require('tailwindcss-animated'),
  ],
  daisyui: {
    themes: ['dracula', "dim"]
  }
}

