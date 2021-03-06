module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      colors: {
        'orangeish': '#fb743e',
        'blueish': '#1687a7'
      },
      spacing: {
        '16': '4rem',
        '18': '4.5rem',
        '20': '5rem',
        '24': '6rem',
        '26': '6.5rem',
        '28': '7rem',
        '30': '7.5rem',
        '32': '8rem',
        '34': '8.5rem',
        '36': '9rem',
        '38': '9.5rem',
        '42': '10.5rem',
        '44': '11rem',
        '52': '13rem',
        '54': '13.5rem',
        '56': '14rem',
        '60': '15rem',
        '62': '15.5rem',
        '68': '17rem',
        '72': '18rem',
        '76': '19rem',
        '80': '20rem',
        '84': '21rem',
        '86': '21.5rem',
        '88': '22rem',
        '90': '22.5rem',
        '92': '23rem',
        '96': '24rem',
        '100': '25rem',
        '100': '25rem',
        '108': '27rem',
        '110': '27.5rem',
        '112': '28rem',
        '116': '29rem',
        '118': '29.5rem',
        '120': '30rem',
        '212': '53rem',
        '216': '54rem',
        '220': '55rem',
        '224': '56rem',
        '228': '57rem',
        '232': '58rem',
        '240': '60rem',
        
      },
    },
  },
  variants: {},
  plugins: [
    require('@tailwindcss/custom-forms'),
  ],
}
