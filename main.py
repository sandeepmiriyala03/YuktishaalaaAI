from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from api.employee_controller import router as employee_router
from api.department_controller import router as department_router

description = """
The intelligent digital charioteer for enterprise graph topologies. Orchestrating live corporate data structures with high-fidelity telemetry.

---

### 🏛️ The Vision
> **"Not a tool, but a torch for your inner Mahabharata."**  
> — *Sandeep Miriyala*

---

### 📡 Live Engine Capabilities:
* **🟢 Production Layer:** Connected directly to the production **Neo graph database**. Live operational records serving current structural states securely. No staging or dummy arrays.
* **🔒 Gateway Protocols:** Strict Cross-Origin Resource Sharing (CORS) rules applied. System endpoints interface exclusively with mapped white-listed development domains.

---
`Engine Status: Active 🚀 | Version: 0.1.0-Alpha | Database: Neo4j Connected 🟢`
"""

app = FastAPI(
    title="🔱 Yuktisárathi Engine Portal | YuktishaalaaAI",
    description=description,
    version="0.1.0-Alpha",
    contact={
        "name": "Sandeep Miriyala (Yuktishaalaa Engineering)",
        "url": "https://aksharatantra.miriyala.in",
    },
    docs_url=None,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian",
        "defaultModelsExpandDepth": -1,
        "docExpansion": "list"
    }
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/logo.png")


@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    return FileResponse("static/sw.js", media_type="application/javascript")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    swagger_html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Core Dashboard",
        swagger_ui_parameters=app.swagger_ui_parameters,
        swagger_favicon_url="/static/logo.png",
    )

    pwa_and_logo_payload = """
    <link rel="manifest" href="/static/manifest.json">
    <link rel="icon" href="/static/logo.png">
    <link rel="apple-touch-icon" href="/static/logo.png">
    <style>
      .swagger-ui .info {
        position: relative;
        padding-right: 240px !important;
      }

      .swagger-ui .info::after {
        content: "";
        position: absolute;
        top: 30px;
        right: 10px;
        width: 200px;
        height: 200px;
        background-image: url('/static/logo.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      }

      @media (max-width: 768px) {
        .swagger-ui .info {
          padding-right: 0 !important;
        }
        .swagger-ui .info::after {
          position: static;
          display: block;
          margin: 20px auto;
          width: 150px;
          height: 150px;
        }
      }

      #pwa-install-btn {
        display: none;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #d4af37, #aa7c11);
        color: #fff;
        border: none;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 6px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
        margin-top: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
      }
      #pwa-install-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212,175,55,0.5);
      }

      #pwa-mobile-banner {
        position: fixed;
        left: 0;
        right: 0;
        bottom: -200px;
        z-index: 9999;
        background: #1a1a1a;
        color: #fff;
        padding: 16px 18px calc(16px + env(safe-area-inset-bottom));
        display: none;
        align-items: center;
        gap: 14px;
        box-shadow: 0 -8px 30px rgba(0,0,0,0.35);
        border-top-left-radius: 18px;
        border-top-right-radius: 18px;
        transition: bottom 0.35s cubic-bezier(.2,.9,.3,1.3);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }
      #pwa-mobile-banner.show {
        bottom: 0;
        display: flex;
      }
      #pwa-mobile-banner .pwa-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background-image: url('/static/logo.png');
        background-size: cover;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
      }
      #pwa-mobile-banner .pwa-text {
        flex: 1;
        min-width: 0;
      }
      #pwa-mobile-banner .pwa-title {
        font-size: 14px;
        font-weight: 700;
        margin: 0 0 2px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      #pwa-mobile-banner .pwa-subtitle {
        font-size: 12px;
        color: #b8b8b8;
        margin: 0;
      }
      #pwa-mobile-banner .pwa-actions {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      #pwa-mobile-banner .pwa-install-cta {
        background: linear-gradient(135deg, #d4af37, #aa7c11);
        color: #fff;
        border: none;
        padding: 9px 16px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 20px;
        cursor: pointer;
        white-space: nowrap;
      }
      #pwa-mobile-banner .pwa-dismiss {
        background: transparent;
        border: none;
        color: #888;
        font-size: 20px;
        line-height: 1;
        padding: 4px 6px;
        cursor: pointer;
      }

      #pwa-ios-sheet {
        position: fixed;
        inset: 0;
        z-index: 10000;
        background: rgba(0,0,0,0.5);
        display: none;
        align-items: flex-end;
        justify-content: center;
      }
      #pwa-ios-sheet.show { display: flex; }
      #pwa-ios-sheet .sheet-inner {
        background: #fff;
        color: #111;
        width: 100%;
        max-width: 480px;
        border-top-left-radius: 18px;
        border-top-right-radius: 18px;
        padding: 22px 22px calc(22px + env(safe-area-inset-bottom));
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        animation: slideUp 0.3s ease;
      }
      @keyframes slideUp {
        from { transform: translateY(40px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
      #pwa-ios-sheet h3 {
        margin: 0 0 14px 0;
        font-size: 16px;
      }
      #pwa-ios-sheet ol {
        margin: 0 0 18px 0;
        padding-left: 20px;
        font-size: 14px;
        line-height: 1.8;
      }
      #pwa-ios-sheet .ios-icon {
        display: inline-block;
        background: #efefef;
        border-radius: 6px;
        padding: 1px 6px;
        font-weight: 600;
      }
      #pwa-ios-sheet button {
        width: 100%;
        background: #1a1a1a;
        color: #fff;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
      }
    </style>

    <div id="pwa-mobile-banner">
      <div class="pwa-icon"></div>
      <div class="pwa-text">
        <p class="pwa-title">Install Yuktisárathi</p>
        <p class="pwa-subtitle">Faster access, works offline</p>
      </div>
      <div class="pwa-actions">
        <button class="pwa-install-cta" id="pwa-install-cta-btn">Install</button>
        <button class="pwa-dismiss" id="pwa-dismiss-btn" aria-label="Dismiss">&times;</button>
      </div>
    </div>

    <div id="pwa-ios-sheet">
      <div class="sheet-inner">
        <h3>📲 Install this app on your iPhone</h3>
        <ol>
          <li>Tap the <span class="ios-icon">Share</span> icon in Safari's toolbar</li>
          <li>Scroll down and tap <span class="ios-icon">Add to Home Screen</span></li>
          <li>Tap <span class="ios-icon">Add</span> in the top right</li>
        </ol>
        <button id="pwa-ios-close-btn">Got it</button>
      </div>
    </div>

    <script>
      (function () {
        const STORAGE_KEY = 'pwa-install-dismissed-at';
        const DISMISS_COOLDOWN_DAYS = 7;

        function recentlyDismissed() {
          const ts = localStorage.getItem(STORAGE_KEY);
          if (!ts) return false;
          const days = (Date.now() - parseInt(ts, 10)) / (1000 * 60 * 60 * 24);
          return days < DISMISS_COOLDOWN_DAYS;
        }

        function markDismissed() {
          localStorage.setItem(STORAGE_KEY, Date.now().toString());
        }

        function isMobile() {
          return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
        }

        function isIOS() {
          return /iPhone|iPad|iPod/i.test(navigator.userAgent) && !window.MSStream;
        }

        function isStandalone() {
          return window.matchMedia('(display-mode: standalone)').matches
            || window.navigator.standalone === true;
        }

        if ('serviceWorker' in navigator) {
          navigator.serviceWorker.register('/sw.js').then((registration) => {
            registration.update();
            if (registration.waiting) {
              registration.waiting.postMessage('CLEAR_CACHE');
            }
            registration.addEventListener('updatefound', () => {
              const newWorker = registration.installing;
              if (newWorker) {
                newWorker.addEventListener('statechange', () => {
                  if (newWorker.state === 'activated') {
                    newWorker.postMessage('CLEAR_CACHE');
                  }
                });
              }
            });
          }).catch((err) => {
            console.warn('Service worker registration failed:', err);
          });
        }

        window.addEventListener('DOMContentLoaded', () => {
          if (isStandalone() || recentlyDismissed()) return;

          const checkInterval = setInterval(() => {
            const descriptionEl = document.querySelector('.info .description .markdown');
            if (descriptionEl) {
              clearInterval(checkInterval);

              if (!isMobile()) {
                const btn = document.createElement('button');
                btn.id = 'pwa-install-btn';
                btn.innerHTML = '📲 Install Yuktisárathi App';
                descriptionEl.insertBefore(btn, descriptionEl.firstChild);

                window.addEventListener('beforeinstallprompt', (e) => {
                  e.preventDefault();
                  window.deferredPrompt = e;
                  btn.style.display = 'inline-flex';
                });

                btn.addEventListener('click', async () => {
                  const promptEvent = window.deferredPrompt;
                  if (!promptEvent) return;
                  btn.style.display = 'none';
                  promptEvent.prompt();
                  await promptEvent.userChoice;
                  window.deferredPrompt = null;
                });
              }
            }
          }, 100);

          if (!isMobile()) return;

          const banner = document.getElementById('pwa-mobile-banner');
          const installCta = document.getElementById('pwa-install-cta-btn');
          const dismissBtn = document.getElementById('pwa-dismiss-btn');
          const iosSheet = document.getElementById('pwa-ios-sheet');
          const iosCloseBtn = document.getElementById('pwa-ios-close-btn');

          function showBanner() {
            requestAnimationFrame(() => banner.classList.add('show'));
          }

          function hideBanner() {
            banner.classList.remove('show');
          }

          if (isIOS()) {
            showBanner();
            installCta.addEventListener('click', () => {
              iosSheet.classList.add('show');
            });
            iosCloseBtn.addEventListener('click', () => {
              iosSheet.classList.remove('show');
            });
          } else {
            window.addEventListener('beforeinstallprompt', (e) => {
              e.preventDefault();
              window.deferredPrompt = e;
              showBanner();
            });

            installCta.addEventListener('click', async () => {
              const promptEvent = window.deferredPrompt;
              if (!promptEvent) return;
              hideBanner();
              promptEvent.prompt();
              await promptEvent.userChoice;
              window.deferredPrompt = null;
            });

            window.addEventListener('appinstalled', hideBanner);
          }

          dismissBtn.addEventListener('click', () => {
            hideBanner();
            markDismissed();
          });
        });
      })();
    </script>
    </body>
    """

    custom_html = swagger_html.body.decode().replace("</body>", pwa_and_logo_payload)
    return HTMLResponse(content=custom_html)


origins = [
    "http://localhost:3000",
    "https://yuktishaalaa-ai.vercel.app",
    "https://aksharatantra.miriyala.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


app.include_router(employee_router)
app.include_router(department_router)