/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "../core/forms.py"],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
    require('tailwindcss-animated'),
  ],
  daisyui: {
    themes: ['dim', "cyberpunk", "lofi"]
  }
}

