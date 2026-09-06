// design-agent.js - Agente de diseno del portfolio de Laura
// Laboratorio en vivo: cambia colores/fuente/tamano/margenes y agrega secciones.
// Comandos: COLOR <hex> | FONT <nombre> | SIZE <px> | MARGIN <valor> | SECTION <titulo> <texto> | THEME <c1> <c2> <c3> <fuente>
// Para revertir cualquier cambio: recargar la pagina (nada queda guardado).
// Basado en el ejemplo-4 de Demos/agente-diseno, adaptado a las variables del portfolio.

function darkenHex(hex) {
  // Oscurece un color hex aprox. 15% para generar el hover del color principal.
  var h = String(hex || "").replace("#", "");
  if (!/^[\da-fA-F]+$/.test(h)) return hex;
  if (h.length === 3) h = h.split("").map(function (c) { return c + c; }).join("");
  if (h.length !== 6) return hex;
  var r = Math.floor(parseInt(h.slice(0, 2), 16) * 0.85);
  var g = Math.floor(parseInt(h.slice(2, 4), 16) * 0.85);
  var b = Math.floor(parseInt(h.slice(4, 6), 16) * 0.85);
  return "#" + [r, g, b].map(function (v) { return v.toString(16).padStart(2, "0"); }).join("");
}

function escapeHtml(text) {
  return String(text || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function designAgent(commandText) {
  var parts = String(commandText || "").trim().split(" ");
  var action = (parts[0] || "").toUpperCase();
  var params = parts.slice(1);
  var root = document.documentElement.style;

  switch (action) {
    case "COLOR":
      root.setProperty("--accent", params[0]);
      root.setProperty("--accent-hover", darkenHex(params[0]));
      return "Color principal actualizado a " + params[0];
    case "FONT":
      document.body.style.fontFamily = params.join(" ");
      return "Tipografia actualizada a " + params.join(" ");
    case "SIZE":
      document.body.style.fontSize = params[0];
      return "Tamano de fuente actualizado a " + params[0];
    case "MARGIN":
      document.body.style.margin = params[0];
      return "Margen general actualizado a " + params[0];
    case "SECTION":
      var titulo = escapeHtml(params[0]);
      var texto = escapeHtml(params.slice(1).join(" "));
      var section = document.createElement("section");
      section.id = titulo.toLowerCase().replace(/[^a-z0-9]+/g, "-");
      section.innerHTML = '<div class="container"><h2>' + titulo + "</h2><p>" + texto + "</p></div>";
      var footer = document.querySelector("footer");
      if (footer) {
        footer.before(section);
      } else {
        document.body.appendChild(section);
      }
      return "Seccion agregada: " + params[0];
    case "THEME":
      if (params[0]) root.setProperty("--accent", params[0]);
      if (params[1]) {
        root.setProperty("--accent-hover", params[1]);
      } else if (params[0]) {
        root.setProperty("--accent-hover", darkenHex(params[0]));
      }
      if (params[2]) root.setProperty("--theme-accent", params[2]);
      if (params[3]) document.body.style.fontFamily = params.slice(3).join(" ");
      return "Tema aplicado con colores " + params[0] + ", " + params[1] + ", " + params[2] + " y fuente " + params.slice(3).join(" ");
    default:
      return "Comando no reconocido. Usa: COLOR, FONT, SIZE, MARGIN, SECTION o THEME.";
  }
}