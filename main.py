from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from api.employee_controller import router as employee_router
from api.department_controller import router as department_router

# Clear markdown description block (safe, no raw styling here to prevent breaking)
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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    swagger_html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Core Dashboard",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )
    
    # Injected CSS payload to dynamically position the logo on the right side of the main title block
    # and custom styles for the PWA action button
    pwa_and_logo_payload = """
    <link rel="manifest" href="/static/manifest.json">
    <style>
      /* Target the Swagger Info panel header and inject the logo on the right side */
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

      /* Stack on mobile layout safely */
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

      /* Premium Cyberpunk Install Button Layout */
      #pwa-install-btn {
        display: none; 
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
    </style>

    <script>
      // Dynamically inject the install button into the description text wrapper area
      window.addEventListener('DOMContentLoaded', () => {
        const checkInterval = setInterval(() => {
          const descriptionEl = document.querySelector('.info .description .markdown');
          if (descriptionEl) {
            clearInterval(checkInterval);
            
            const btn = document.createElement('button');
            btn.id = 'pwa-install-btn';
            btn.innerHTML = '📲 Install Yuktisárathi App';
            
            // Insert it at the top of the description section
            descriptionEl.insertBefore(btn, descriptionEl.firstChild);
            
            // Listen for browser PWA deployment prompt
            window.addEventListener('beforeinstallprompt', (e) => {
              e.preventDefault();
              window.deferredPrompt = e;
              btn.style.display = 'inline-block';
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
        }, 100);
      });
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