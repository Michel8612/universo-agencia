import { NextRequest } from "next/server";

// Devuelve el widget JS embeddable que los clientes ponen en su web
export async function GET(
  req: NextRequest,
  { params }: { params: { businessId: string } }
) {
  const { businessId } = params;
  const host = req.headers.get("host") || "localhost:3000";
  const protocol = host.includes("localhost") ? "http" : "https";
  const baseUrl = `${protocol}://${host}`;

  const widgetScript = `
(function() {
  var BUSINESS_ID = "${businessId}";
  var API_URL = "${baseUrl}";

  // Crear botón flotante
  var btn = document.createElement("button");
  btn.id = "ai-chat-btn";
  btn.innerHTML = "💬";
  btn.style.cssText = "position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:#6366f1;color:white;font-size:24px;border:none;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.3);z-index:9999;transition:transform 0.2s";
  btn.onmouseenter = function() { this.style.transform = "scale(1.1)"; };
  btn.onmouseleave = function() { this.style.transform = "scale(1)"; };
  document.body.appendChild(btn);

  // Crear iframe del chat
  var iframe = document.createElement("iframe");
  iframe.src = API_URL + "/widget/" + BUSINESS_ID;
  iframe.style.cssText = "position:fixed;bottom:96px;right:24px;width:380px;height:550px;border:none;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.2);z-index:9998;display:none;";
  document.body.appendChild(iframe);

  btn.onclick = function() {
    var visible = iframe.style.display !== "none";
    iframe.style.display = visible ? "none" : "block";
    btn.innerHTML = visible ? "💬" : "✕";
  };
})();
`;

  return new Response(widgetScript, {
    headers: {
      "Content-Type": "application/javascript",
      "Cache-Control": "public, max-age=3600",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
