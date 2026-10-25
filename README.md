# ♻️ AI Waste Sorting Assistant

Upload a photo of a waste item. A pretrained Hugging Face image-classification model suggests the waste type, and the app shows disposal and recycling guidance with safety warnings.

## Problem statement
Wrong waste disposal contaminates recycling and harms the environment. Many people are unsure which bin an item belongs in. This project gives quick, free, AI-assisted guidance.

## Features
- Drag-and-drop / file upload (JPG, JPEG, PNG) with preview, type and size validation
- Real AI classification (no fake or hardcoded predictions)
- Top-3 predictions, confidence estimate, uncertainty handling ("Not sure" instead of a wrong guess)
- Disposal + recycling guidance and safety warnings (broken glass, batteries, hazardous items)
- Analysis history (SQLite, text only — **images are never stored**), clear history
- Feedback on wrong predictions, waste segregation guide, recycling tips
- Responsive green UI

## Technology stack
React + Vite · Flask · Transformers + PyTorch · Pillow · SQLite

## Architecture
```
Browser (React)  --multipart POST /api/classify-->  Flask API
                                                     |- validates file (type, size, real image via Pillow)
                                                     |- classifier.py: Hugging Face model -> top-3 + confidence
                                                     |- disposal_guidance.py: label -> advice
                                                     '- database.py: SQLite history (text only)
```

## The AI model (important, please read)
Default: [`prithivMLmods/Trash-Net`](https://huggingface.co/prithivMLmods/Trash-Net), a SigLIP2-based image classifier fine-tuned on the TrashNet dataset.
Its **actual labels** are: `cardboard, glass, metal, paper, plastic, trash`. Verify them yourself:
```
cd backend
python check_labels.py
```
- It has **no classes** for batteries, organic/food waste, or clothing & shoes, so the app does not claim to detect them. Items in those groups may be wrongly labelled; the "General waste" advice warns about this.
- TrashNet photos are single items on plain backgrounds. Expect lower accuracy on cluttered real-world photos. The published accuracy is on the TrashNet test split, **not** on your photos, and we have not tested it on real-world waste.
- Low confidence, or a small gap between the top two guesses, produces a "Not sure" result (`MIN_CONFIDENCE`, `MIN_MARGIN` in `.env`).
- To try another model, set `MODEL_ID` in `.env` (for example `tribber93/my-trash-classification`, a ViT fine-tuned on the same six classes). Then update `disposal_guidance.py` if its labels differ. To evaluate any model, run it on ~20–50 of your own labelled photos and count correct answers.
- First run downloads the model from Hugging Face (needs internet; cached afterwards).

## Setup on Windows 11 (PowerShell)

### 1. Folders
Extract the zip, or create the folders yourself, then:
```
cd AI-Waste-Sorting-Assistant
```
### 2–3. Python environment + dependencies
Install Python 3.10–3.12 from python.org first.
```
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
If activation is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
Smaller CPU-only PyTorch (x64 laptops): `pip install torch --index-url https://download.pytorch.org/whl/cpu` before the line above.

**Snapdragon / ARM laptop:** PyTorch support for Windows on ARM depends on the version and Python build. If `pip install torch` fails, install the **64-bit x64 Python** (it runs under Windows emulation, slower but works), check pytorch.org for current ARM64 wheels, or run the backend in WSL / Google Colab. Check these steps on your own machine.

### 4. Frontend (Vite)
This zip already contains a Vite React project, so just:
```
cd ..\frontend
npm install
```
(Needs Node.js LTS from nodejs.org.) If you prefer starting fresh: `npm create vite@latest frontend -- --template react`, then copy the `src/` files and `index.html` over.

### 5. Run the backend
```
cd backend
venv\Scripts\Activate.ps1
python app.py
```
Open http://127.0.0.1:5000 — you should see JSON status.

### 6. Run the frontend (second terminal)
```
cd frontend
npm run dev
```
Open http://localhost:5173.

### 7. Test everything
1. Upload a clear photo of a plastic bottle or cardboard box and click **Analyze Waste** (first run is slow: model download).
2. Check the result, top-3 bars and safety text.
3. Upload a `.gif` or a huge file: you should see a friendly error.
4. Stop the backend and analyze again: you should see "Cannot reach the server".
5. Open **History**, click feedback buttons, and **Clear history**.

### 8. Common errors
| Problem | Fix |
|---|---|
| "Cannot reach the server" | Backend not running, or port differs. Check `VITE_API_URL` in `frontend/.env`. |
| CORS error in browser console | Add your frontend URL to `CORS_ORIGINS` in `backend/.env`, restart backend. |
| `ModuleNotFoundError` | Virtual environment not activated, or `pip install -r requirements.txt` failed. |
| 503 "model not available" | No internet on first run, or old `transformers`. Run `pip install -U transformers` and `python check_labels.py` to see the real error. |
| Port 5000 in use | Set `PORT=5001` in `.env` and update `VITE_API_URL`. |
| `npm` not recognised | Install Node.js LTS and reopen the terminal. |

## API
| Method | Route | Description |
|---|---|---|
| GET | `/` | API + model status |
| POST | `/api/classify` | multipart form field `image` → result JSON |
| GET | `/api/history` | last 50 analyses |
| DELETE | `/api/history` | clear history |
| POST | `/api/feedback` | JSON `{ "id": 1, "correct": false }` |

Example response of `/api/classify`: `{ success, id, label, category, confidence, uncertain, top_predictions[], guidance{...}, disclaimer }`. Errors: `{ success:false, error:"..." }`.

## GitHub
```
cd AI-Waste-Sorting-Assistant
git init
git add .
git commit -m "Initial commit: AI Waste Sorting Assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/AI-Waste-Sorting-Assistant.git
git push -u origin main
```
`.gitignore` already excludes `venv`, `node_modules`, `.env` and the database. Add screenshots to a `screenshots/` folder and link them below.

## Deployment (free options change often; check current limits)
- **Frontend:** Vercel or Netlify. Root directory `frontend`, build `npm run build`, output `dist`. Set env var `VITE_API_URL` to your backend URL.
- **Backend:** needs ~1–2 GB RAM because of PyTorch. Hugging Face Spaces (Docker or Gradio-free Flask in a Docker Space) or Render/Railway are options; free tiers may be too small, sleep when idle, and give slow first requests. Use `waitress-serve --port=%PORT% app:app` (Windows) or `gunicorn app:app` (Linux hosts). Set `CORS_ORIGINS` to your deployed frontend URL. Free hosts often reset the SQLite file on restart.

## Screenshots
_Add screenshots here after running the app._

## Limitations
- Only six model classes; no battery, organic or clothing detection.
- Trained on clean TrashNet images; may fail on cluttered or real-world photos.
- One item per photo works best. Guidance is general, not local law.
- Confidence is an estimate, not accuracy.

## Future improvements
Fine-tune on a larger real-world dataset (e.g. TACO or a 12-class garbage dataset) to add organic, battery and clothing classes; city-specific rules; user accounts; Docker setup; automated tests.
