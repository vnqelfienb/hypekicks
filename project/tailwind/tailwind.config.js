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
    function({ addUtilities }) {
      addUtilities({
        '.scrollbar-hidden': {
          'scrollbar-width': 'none', /* Firefox */
          '-ms-overflow-style': 'none', /* IE and Edge */
        },
        '.scrollbar-hidden::-webkit-scrollbar': {
          display: 'none', /* Chrome, Safari, Opera */
        },
      });
    },
  ],
  daisyui: {
    themes: ['dracula', "dim"]
  }
}

