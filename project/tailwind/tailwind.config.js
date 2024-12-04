/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "../**/forms.py"],
  theme: {
    extend: {
      fontFamily: {
        bokor: ['Bokor', 'system-ui'],
        fira: ['Fira Sans', 'sans-serif'],
        doto: ['Doto', 'sans-serif'],
        robotoCondensed: ['Roboto Condensed', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif']
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('tailwindcss-animated'),
  ],
  daisyui: {
    themes: ['dracula', "dim"]
  }
}

