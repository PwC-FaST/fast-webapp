/**
 * F7 Build Configuration
 * for custom FaST theme (cf http://framework7.io/docs/custom-build.html#custom-build)-
 */

const config = {
  target: "universal",
  rtl: false,
  components: [
    // Modals
    "dialog",
    "popup",
    //'login-screen',
    //'popover',
    //'actions',
    "sheet",
    "toast",

    // Loaders
    "preloader",
    "progressbar",

    // List Components
    "sortable",
    "swipeout",
    //'accordion',
    "contacts-list",
    //'virtual-list',
    //'list-index',

    // Timeline
    //'timeline',

    // Tabs
    //'tabs',

    // Panel
    "panel",

    // Card
    //'card',

    // Chip
    //'chip',

    // Form Components
    //'form',
    "input",
    "checkbox",
    "radio",
    "toggle",
    "range",
    "stepper",
    "smart-select",

    // Grid
    "grid",

    // Pickers
    //'calendar',
    //'picker',

    // Page Components
    //'infinite-scroll',
    "pull-to-refresh",
    //'lazy',

    // Data table
    //'data-table',

    // FAB
    //'fab',

    // Searchbar
    "searchbar",

    // Messages
    "messages",
    "messagebar",

    // Swiper
    //'swiper',

    // Photo Browser
    //'photo-browser',

    // Notifications
    //'notification',

    // Autocomplete
    //'autocomplete',

    // Tooltip
    //'tooltip',

    // Gauge
    //'gauge',

    // VI Video Ads
    //'vi',

    // Elevation
    //'elevation',

    // Typography
    "typography"
  ],
  darkTheme: true,
  themes: ["ios", "md"],
  ios: {
    themeColor: "#528A97",
    colors: {
      red: "#EE5158",
      green1: "#427F6D",
      green2: "#509A84",
      green3: "#5FB99F",
      blue1: "#528A97",
      blue2: "#68ACBC",
      blue3: "#7BCCDF",
      yellow: "#F3C86A",
      orange: "#C59563",
      //gray1: '#3B4A5E',
      gray2: "#6B7B91",
      //gray3: '#8491A4',
      gray4: "#A4AFBE",
      //gray5: '#C7CFDA',
      gray6: "#E6EAEE",
      white: "#ffffff",
      black: "#000000",
      purple1: "#5856d6",
      purple2: "#B279D5"
    }
  },
  md: {
    themeColor: "#528A97",
    colors: {
      red: "#EE5158",
      //green1: '#427F6D',
      green2: "#509A84",
      //green3: '#5FB99F',
      //blue1: '#528A97',
      //blue2: '#68ACBC',
      //bue3: '#7BCCDF',
      yellow: "#F3C86A",
      //orange: '#C59563',
      //gray1: '#3B4A5E',
      gray2: "#6B7B91",
      //gray3: '#8491A4',
      gray4: "#A4AFBE",
      //gray5: '#C7CFDA',
      gray6: "#E6EAEE",
      white: "#ffffff",
      black: "#000000"
      //purple1: '#5856d6',
      //purple2: '#B279D5'
    }
  }
};

module.exports = config;
