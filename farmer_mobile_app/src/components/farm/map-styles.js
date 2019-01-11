// Styles for rendering vector layers

const lpisStyleSelected = {
  fill: true,
  weight: 4,
  fillColor: "#F3C86A",
  color: "#F3C86A",
  fillOpacity: 0.5,
  opacity: 0.9
};

const lpisStylePrimary = {
  fill: true,
  weight: 4,
  fillColor: "#ffffff",
  color: "#ffffff",
  fillOpacity: 0.5,
  opacity: 0.7
};

const lpisStyleSecondary = {
  fill: true,
  weight: 3,
  fillColor: "#ffffff",
  color: "#ffffff",
  fillOpacity: 0.2,
  opacity: 0.4
};

const lpisStyleDefault = {
  fill: true,
  weight: 1,
  fillColor: "#8491A4",
  color: "#8491A4",
  fillOpacity: 0.1,
  opacity: 0.3
};

const lpisStyleHidden = {
  fill: false,
  opacity: 0
};

const hydroStyle = {
  fill: true,
  weight: 3,
  fillColor: "#06cccc",
  color: "#06cccc",
  fillOpacity: 0.4,
  opacity: 0.8
};

const natura2000Style = {
  fill: true,
  weight: 2,
  fillColor: "#53e033",
  color: "#53e033",
  fillOpacity: 0.4,
  opacity: 0.8
};

export {
  lpisStyleSelected,
  lpisStylePrimary,
  lpisStyleSecondary,
  lpisStyleDefault,
  lpisStyleHidden,
  hydroStyle,
  natura2000Style
};
