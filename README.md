# BIM-AI Cross-Platform Automation Suite: Real-Time QTO & Cost Engine

An enterprise-grade, **Stateful Multi-Agent BIM Entegrasyon Platform** designed to automate dynamic Quantity Take-Off (QTO), real-time cost estimations, and cross-platform geometry routing. The platform establishes a live, bi-directional asynchronous data bridge between desktop viewports (**Autodesk Revit & Rhino**) and a stateful AI Orchestration Core powered by **Anthropic Claude 3.5 Sonnet / Llama 3.1**, backed by a zero-hallucination execution pipeline.

---

## 🏗️ System Architecture

The engine is engineered under a decoupled **Hybrid AI-Code Architecture** adhering strictly to the **Single Responsibility Principle (SRP)**. The LLM is restricted to acting as a semantic conductor, while all database query operations, file mutations, and structural element tracking are handled by deterministic backend pipelines.

```text
┌────────────────────────────────────────────────────────┐
│             CENTRAL STANDALONE WEB PANEL               │ (React.js UI / Unified Chat Canvas)
└───────────────────────────┬────────────────────────────┘
                            │ REST API / Secure JWT Session Token
┌───────────────────────────▼────────────────────────────┘
│          STATEFUL AI ORCHESTRATOR (FastAPI)            │ (Central Brain / System Router)
└───────────────┬────────────────────────┬───────────────┘
                │                        │
                ▼ [State & Memory Pool]  ▼ [Central Relational Data]
┌───────────────────────────────┐ ┌───────────────────────────────┐
│         Redis Cache           │ │       PostgreSQL Server       │
│  (Multi-Turn Conversation Log)│ │ (Price Catalogs & Index DB)   │
└───────────────────────────────┘ └───────────────────────────────┘
                │
                ▼ [Asynchronous REST JSON Streaming over Port 8080]
┌────────────────────────────────────────────────────────┐
│     HEADLESS DESKTOP ENGINE (C# .NET 8.0 PLUGIN)       │ (Revit API / RhinoCommon Workers)
└────────────────────────────────────────────────────────┘
```

1. **Headless Execution Layer (C# .NET 8.0 / Revit API):** 
   Operates silently as a background service application (`IExternalApplication`) upon desktop boot. To completely prevent main thread deadlocks and UI viewport freezing, it triggers the native Revit `Idling` event hook to safely serialize building analytics into a thread-safe static memory cache (`CachedWindowData`), streaming real-time JSON element payload arrays over port `8080`.
2. **Intelligent Routing Core (Python FastAPI):** 
   Registers atomic data worker tools as structured `JSON Schemas`. The orchestrator intercepts the incoming prompt, invokes advanced **Tool Calling**, and maps user architectural intents into strict execution values.
3. **Deterministic Strategy Engine:** 
   Eliminated LLM hallucination risks in core financial calculations. The Python gateway handles structural arguments (e.g., `COUNT_ONLY`, `GENERATE_COST_EXCEL`, `CLASSIFY_ONLY`) using a **Strategy Design Pattern** that offloads matrix data mashups to high-precision Python Pandas logic blocks.
4. **Stateful Conversation Pool:** 
   Leverages an in-memory **Redis Cache** database layer to hold session states across conversational threads. Architects can iteratively refine data requests (e.g., *"Find all windows,"* followed by *"Now classify them by type"* or *"Generate the cost sheet"*) without losing the active context tree.

---

## 🚀 Core Platform Features

- **Zero-Hallucination Guardrails:** The LLM does not compute prices or count elements. It acts as a semantic routing layer; the backend calculates financial bills of quantities with 100% mathematical accuracy.
- **Corporate Privacy & Air-Gapped Readiness:** Designed to switch seamlessly between cloud endpoints (**Claude 3.5 Sonnet**) and secure, local enterprise sunucus environments (**Ollama / Llama-3-70B**) to isolate proprietary corporate files and building geometries on the local area network (LAN).
- **Cross-Platform Scalability:** Built on a unified headless asset framework, enabling a single natural language command to orchestrate workflows across multiple CAD environments simultaneously.

---

## 📊 Sample Production Execution Workflow

**Natural Language Command Input:**
> *"Calculate the total cost analysis for all windows in the entire project using our corporate price directory and output the spreadsheet."*

**Automated Orchestration Pipeline Logs:**
```bash
>> [State Verification]: Session 'sess_44e2b8' verified. Active project context initialized.
>> [AI Orchestrator]: Tool called: 'fetch_live_bim_elements'
>> [Revit API Success]: Connected to active viewport window session. Captured 106 elements instantly.
>> [LLM Strategy Triggered]: Argument 'sub_action' mapped to 'GENERATE_COST_EXCEL'
>> [Platform Output]: UniqueId hashes mapped against central directory matrix. Total cost: 477,000 TL.
>> [Platform Output]: 'Nihai_Hakedis_Raporu.xlsx' successfully written to disk root.
```

---

## 📂 Repository Directory Layout

```text
BIM-AI-Automation-Platform/
│
├── .gitignore                      # Excludes bin/, obj/, venv/, and generated .xlsx assets
├── README.md                       # Platform documentation
├── BIM-AI-Automation.sln           # Visual Studio Solution File
│
├── src/
│   ├── RevitPlugin/                # Headless C# Class Library Project (.NET 8.0)
│   │   ├── AppMain.cs              # Global background server runtime registration
│   │   ├── LiveHttpServer.cs       # Thread-safe async socket engine & data cache
│   │   └── RevitPlugin.csproj      # Clean SDK-style reference manager
│   │
│   └── PythonBackend/              # Python FastAPI & AI Analytics Engine
│       ├── app.py                  # Stateful Multi-Tool Router & Pandas Matrix Engine
│       ├── fiyat_katalogu.xlsx     # Corporate pricing index directory file
│       └── requirements.txt        # Frozen library manifests (fastapi, pandas, ollama)
```

---

## ⚙️ Installation & Testing

### 1. C# Plugin Deployment
Compile the `RevitPlugin.csproj` in Visual Studio under x64 configuration. Move the output `.dll` and your manifest `.addin` file into the target directory:
```text
%USERPROFILE%\AppData\Roaming\Autodesk\Revit\Addins\2027\
```

### 2. Python Server Boot
Activate your virtual environment and launch your fast API server gateway:
```bash
cd src/PythonBackend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
*The endpoint server will spin up on `http://127.0.0.1:8000`. Open `/docs` in your browser to instantly interact with the live AI testing ground tool.*
