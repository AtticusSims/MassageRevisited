# Dynamic Migration Prompt — The Model is the Massage

## Session Objective

Migrate the book review site from static GitHub Pages to a dynamic site on Hostinger at `http://the-model-is-the-massage.com/`. Add server-side persistence so that multiple users can make selections, leave comments, and see each other's input in real-time (on refresh).

---

## 1. Current Architecture (Static)

### Hosting
- **Current**: GitHub Pages, deployed from `mcluhan-analysis/docs/` via `.github/workflows/pages.yml`
- **Target**: Hostinger Premium Web Hosting (shared, PHP available)
  - Domain: `the-model-is-the-massage.com` (registered March 6, 2026, active)
  - Addon website already created, root: `/home/u622598818/domains/the-model-is-the-massage.com/public_html`
  - **DNS note**: Nameservers are currently `ns1.dns-parking.com` / `ns2.dns-parking.com` — may need pointing to Hostinger
  - Hostinger MCP tools are available for direct file upload (use `hosting_deployStaticWebsite` or `hosting_deployWordpressPlugin` etc.)
  - Order ID: 52265562

### File Structure
```
mcluhan-analysis/docs/           ← deployment root
├── index.html         (95 KB)   ← Main review interface (intro + spread viewer)
├── authoring.html     (97 KB)   ← Authoring review interface
├── review.html        (67 KB)   ← Layout review interface
├── v2_comparison.html (63 KB)   ← Comparison viewer
├── style.css          (37 KB)   ← Shared dark-theme CSS
├── data/                        ← 95 JSON files (~2.9 MB total)
│   ├── authoring_output.json    (877 KB) — 85 spreads with text options A/B/C
│   ├── image_metadata.json      (140 KB) — image options per spread
│   ├── review_selections.json   (37 KB)  — APS reviewer selections & ratings
│   ├── revised_drafts.json      (20 KB)  — finalized text/caption/image overrides
│   ├── framework.json           (56 KB)  — intellectual framework
│   ├── index.json               (13 KB)  — navigation index
│   ├── meta.json                (49 KB)  — project metadata
│   └── spread_001.json ... spread_085.json  (~18 KB each)
├── images/                      ← 247 image files (~73 MB)
│   └── v2/                      ← Additional assets
└── reports/                     ← Analysis reports
```

### Technology Stack
- **Frontend**: Vanilla JS, HTML5, CSS3 (no frameworks, no build step)
- **Data**: All JSON, loaded via `fetch()` at page init
- **Persistence**: `localStorage` only — everything is browser-local, single-user
- **Fonts**: 14 Google Fonts loaded via stylesheet link
- **Theme**: Dark theme with gold accent (`--bg: #1a1a1a`, `--accent: #e8a838`)

---

## 2. The Three Pages and Their Interactivity

### 2a. index.html — Main Review Interface

**Purpose**: Landing page with project intro + interactive spread viewer with tabs (Analysis, Visual, Planning).

**Current localStorage keys**:
- `mcluhan_review` — Approve/Flag status per spread: `{ spread_id: { status: "approved"|"flagged" } }`
- `mcluhan_feedback` — Planning tab feedback notes: `{ spread_id: [{ text, timestamp }] }`
- `mcluhan_feedback_analysis` — Analysis tab feedback notes (same schema)
- `mcluhan_feedback_visual` — Visual tab feedback notes (same schema)

**User interactions that need persistence**:
| Action | Current Storage | What Needs to Change |
|--------|----------------|---------------------|
| Approve/Flag spread (Y/F keys or buttons) | `mcluhan_review` in localStorage | Save to server per-user |
| Add feedback note (3 sections: analysis, visual, planning) | `mcluhan_feedback*` in localStorage | Save to server per-user; show all users' notes in panel |
| Delete feedback note | localStorage splice | Server-side delete (own notes only) |
| Export review | Downloads JSON | Can keep as-is (client-side export) |

**Feedback note rendering** — `buildFeedbackHTML(section)` creates:
```html
<div class="section plan-section feedback-section">
  <div class="section-header">Feedback</div>
  <div class="feedback-input">
    <textarea id="feedbackNote_{section}" placeholder="Add feedback note..." rows="2"></textarea>
    <button class="feedback-add-btn" onclick="addFeedbackNote('{section}')">Add Note</button>
  </div>
  <div id="feedbackNotes_{section}"></div>  <!-- notes rendered here -->
</div>
```

Each note renders as:
```html
<div class="feedback-note">
  <div class="feedback-note-text">{text}</div>
  <div class="feedback-note-meta">
    <span class="feedback-date">{date}</span>
    <button class="feedback-delete" onclick="deleteFeedbackNote({i},'{section}')">&times;</button>
  </div>
</div>
```

**Key functions**: `addFeedbackNote(section)`, `deleteFeedbackNote(index, section)`, `renderFeedbackNotes(section)`, `getFeedbackData(section)`, `saveFeedbackData(section, fbData)`, `setReviewStatus(spreadId, status)`, `getReviewData()`

---

### 2b. review.html — Layout Review

**Purpose**: View rendered book spreads with layout preview + original scan comparison. Rate layouts and add review notes.

**Current localStorage keys**:
- `review_notes_v1` — Free-text notes per spread: `{ spread_id: "note text" }`

**Data loaded at init**:
```javascript
data = await fetch('data/authoring_output.json')        // 85 spreads with text options
imageMetadata = await fetch('data/image_metadata.json')  // image options per spread
revisedDrafts = await fetch('data/revised_drafts.json')  // finalized overrides
reviewData = (await fetch('data/review_selections.json')).selections  // APS selections
```

**User interactions that need persistence**:
| Action | Current Storage | What Needs to Change |
|--------|----------------|---------------------|
| Type review notes in textarea | `review_notes_v1` localStorage, auto-saves on input | Save to server per-user |
| Select image thumbnail | `currentImageIdx` page variable only (not persisted!) | Save to server per-user |
| Export notes | Downloads JSON | Can keep |

**Key functions**: `saveNote()`, `selectImage(sid, idx)`, `renderSpread(index)`, `resolveTextForSpread(spread)`

**APS review data display** (read-only from `review_selections.json`):
- Star ratings shown in `.aps-ratings` section
- Reviewer notes shown in `.aps-notes` section
- These are currently read-only — they come from the JSON file

---

### 2c. authoring.html — Authoring Review

**Purpose**: Compare text options A/B/C for each spread, select preferred text, rate quality, choose images, add notes.

**Current localStorage keys**:
- `authoring_selections_v2` — All user choices: `{ spread_id: { text: "a", quality_a: 3, quality_b: 2, selectedImage: 1, notes: "..." } }`
- `authoring_fonts` — Font picker state: `{ display: "Space Grotesk", body: "Inter", caption: "Source Serif 4" }`

**Data loaded at init** (same 4 files as review.html):
```javascript
data = await fetch('data/authoring_output.json')
imageMetadata = await fetch('data/image_metadata.json')
revisedDrafts = await fetch('data/revised_drafts.json')
reviewData = await fetch('data/review_selections.json')
```

**User interactions that need persistence**:
| Action | Current Storage | What Needs to Change |
|--------|----------------|---------------------|
| Select text option (A/B/C or Enter key) | `selections[sid].text` in localStorage | Save to server per-user; update page to show selection |
| Rate option quality (1-3 buttons) | `selections[sid].quality_{optId}` in localStorage | Save to server per-user |
| Select image from strip | `selections[sid].selectedImage` in localStorage | Save to server per-user |
| Type reviewer notes | `selections[sid].notes` in localStorage | Save to server per-user; show all users' notes |
| Change fonts | `authoring_fonts` in localStorage | Keep client-side (personal preference) |
| Export selections | Downloads JSON | Can keep |

**Key functions**: `selectOption(sid, optId)`, `setQuality(sid, optId, rating)`, `selectImage(sid, idx)`, `saveNotes()`, `saveSelections()`, `buildOptionCards(spread)`, `renderSpreadLayout(spread, opt)`

**Selection card UI**: Options are shown as cards with:
- Header (option ID + label + APS stars if rated)
- Meta tags (strategy, voice register, word count)
- Text preview (body text)
- Quality rating buttons (3=green, 2=orange, 1=red)
- View/Select action buttons

---

## 3. Required Changes

### 3a. Backend API (PHP on Hostinger)

Create a simple PHP REST API with flat-file JSON storage (no database needed for this scale). All API endpoints go in an `api/` directory.

**Storage structure** (server-side):
```
api/
├── index.php          ← API router
├── storage/
│   ├── users.json     ← { "user1": { created: "...", displayName: "User 1" }, ... }
│   ├── selections/
│   │   ├── user1/
│   │   │   ├── authoring.json    ← text/image/rating selections
│   │   │   ├── review_notes.json ← layout review notes
│   │   │   └── review_status.json ← approve/flag status
│   │   └── user2/
│   │       └── ...
│   └── feedback/
│       ├── spread_001_planning.json  ← [{ user, text, timestamp }]
│       ├── spread_001_analysis.json
│       ├── spread_001_visual.json
│       └── ...
```

**API Endpoints needed**:

```
GET  /api/users                              → list all usernames
POST /api/users          { name }            → create new user
GET  /api/users/{user}/selections/{page}     → get user's selections for a page type
POST /api/users/{user}/selections/{page}     → save user's selections (full replace)

GET  /api/feedback/{spreadId}/{section}       → get all feedback notes for spread+section (all users)
POST /api/feedback/{spreadId}/{section}       → add a note { user, text }
DELETE /api/feedback/{spreadId}/{section}/{index}  → delete a specific note (own only)

GET  /api/users/{user}/review-status          → get user's approve/flag data
POST /api/users/{user}/review-status          → save approve/flag data
```

**Security**: This is a private review tool, not public-facing. Basic validation is sufficient. No authentication beyond username selection. Protect `storage/` directory with `.htaccess` deny from all.

### 3b. Frontend — User Dropdown (All Pages)

Add a persistent user selector to the header of ALL pages (index.html, review.html, authoring.html):

```html
<div class="user-selector">
  <select id="userSelect" onchange="switchUser()">
    <option value="">Select user...</option>
    <!-- populated from GET /api/users -->
  </select>
  <button onclick="createUser()" title="New user">+</button>
</div>
```

- On page load, fetch user list from API and populate dropdown
- Store selected username in `localStorage` key `current_user` so it persists across page navigation
- If no user selected, show a prompt/overlay requiring selection before interaction
- Username appears on all comments/notes the user creates

### 3c. Frontend — index.html Changes

1. **Replace `getReviewData()`/`setReviewStatus()`**: Instead of `localStorage.getItem('mcluhan_review')`, use:
   - `GET /api/users/{user}/review-status` on load
   - `POST /api/users/{user}/review-status` on change

2. **Replace `getFeedbackData()`/`saveFeedbackData()`**: Instead of `localStorage`, use:
   - `GET /api/feedback/{spreadId}/{section}` when rendering a spread's feedback panel
   - `POST /api/feedback/{spreadId}/{section}` when adding a note
   - `DELETE /api/feedback/{spreadId}/{section}/{index}` when deleting

3. **Show all users' feedback**: `renderFeedbackNotes(section)` should display notes from ALL users, with username shown:
   ```html
   <div class="feedback-note">
     <div class="feedback-note-text">{text}</div>
     <div class="feedback-note-meta">
       <span class="feedback-user">{username}</span>
       <span class="feedback-date">{date}</span>
       <!-- only show delete button if note belongs to current user -->
       <button class="feedback-delete" onclick="deleteFeedbackNote(...)">×</button>
     </div>
   </div>
   ```

### 3d. Frontend — review.html Changes

1. **Replace `saveNote()`**: Instead of `localStorage.setItem('review_notes_v1', ...)`, use:
   - `POST /api/users/{user}/selections/review` (debounced, saves on pause in typing)
   - `GET /api/users/{user}/selections/review` on load

2. **Image selection**: Persist `selectImage(sid, idx)` choice via the same selections endpoint

3. **The Reviewer Notes panel** (`#reviewNotes` textarea): Each user has their own notes. Optionally show a read-only list of other users' notes below the textarea.

### 3e. Frontend — authoring.html Changes

1. **Replace `saveSelections()`**: Instead of `localStorage.setItem('authoring_selections_v2', ...)`, use:
   - `POST /api/users/{user}/selections/authoring` (debounced)
   - `GET /api/users/{user}/selections/authoring` on load

2. **Text option selection** (`selectOption`): When a user selects option A/B/C:
   - Save to server immediately
   - Re-render the spread layout with their selection
   - Selection is per-user (different users can select different options)

3. **Quality ratings** (`setQuality`): Save to server immediately per-user

4. **Image selection** (`selectImage`): Save to server immediately per-user

5. **Notes** (`saveNotes`): Save to server (debounced). Show all users' notes in the panel with usernames.

6. **Font selections**: Keep in localStorage (personal preference, no need to share)

### 3f. Data Files — Keep Static

The following files remain static JSON served as-is (they are the source content, not user data):
- `authoring_output.json` — the 85 spreads with text options
- `image_metadata.json` — image options metadata
- `revised_drafts.json` — finalized text overrides (author-controlled)
- `review_selections.json` — the APS reviewer's original selections (read-only reference data)
- `framework.json`, `meta.json`, `index.json` — reference data
- All `spread_*.json` files — analysis data
- All images — static assets

---

## 4. Deployment Steps

### 4a. Prepare Archive
1. Copy all current `docs/` content
2. Add the new `api/` directory with PHP backend
3. Add `.htaccess` rules:
   - Deny direct access to `api/storage/`
   - Ensure `api/` routes work
   - Set appropriate CORS headers if needed (probably not, same-origin)
4. Archive everything

### 4b. Deploy to Hostinger
Use the Hostinger MCP tool `hosting_deployStaticWebsite`:
```
domain: "the-model-is-the-massage.com"
archivePath: path to the zip archive
```

### 4c. DNS
The domain nameservers may need updating from `dns-parking.com` to Hostinger's actual hosting nameservers. Check via:
- `hosting_listWebsitesV1` to confirm the website addon exists
- `domains_getDomainDetailsV1` to check nameserver status
- `domains_updateDomainNameserversV1` if needed

### 4d. Verify
- Test that static pages load at `http://the-model-is-the-massage.com/`
- Test that `api/users` endpoint responds
- Test user creation and selection persistence
- Test feedback notes across users

---

## 5. Key Implementation Notes

### Pattern for API Integration

The cleanest approach is to create a shared `api.js` utility:

```javascript
const API_BASE = '/api';

async function apiGet(path) {
  const resp = await fetch(`${API_BASE}${path}`);
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

async function apiPost(path, data) {
  const resp = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

function getCurrentUser() {
  return localStorage.getItem('current_user') || '';
}
```

This can be inlined in each HTML file (they're self-contained single-file apps) or loaded as a shared script.

### Debouncing

For notes/textarea inputs that auto-save, use a debounce pattern (300-500ms) to avoid hammering the API on every keystroke:

```javascript
let saveTimer = null;
function debouncedSave(fn, delay = 400) {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(fn, delay);
}
```

### Backward Compatibility

Keep the localStorage code as a fallback. If the API is unreachable, the pages should still function using localStorage (degraded single-user mode). Load from API first, fall back to localStorage.

### File Permissions on Hostinger

The `api/storage/` directory needs to be writable by the PHP process. On Hostinger shared hosting, this should work by default for directories under `public_html/`, but the PHP script should `chmod` or create directories as needed.

---

## 6. Files to Reference

When implementing, read these files for the full current code:

| File | What to Look For |
|------|-----------------|
| `docs/index.html` | `getFeedbackData()`, `saveFeedbackData()`, `addFeedbackNote()`, `renderFeedbackNotes()`, `buildFeedbackHTML()`, `getReviewData()`, `setReviewStatus()`, `exportRevisionPrompt()` |
| `docs/review.html` | `saveNote()`, `selectImage()`, `renderSpread()`, `resolveTextForSpread()`, `buildSyntheticOption()`, `getImageUrl()`, `buildImageElement()` |
| `docs/authoring.html` | `saveSelections()`, `selectOption()`, `setQuality()`, `selectImage()`, `saveNotes()`, `buildOptionCards()`, `renderSpreadLayout()`, `exportSelections()` |
| `docs/data/review_selections.json` | APS review data schema (read-only reference) |
| `docs/data/revised_drafts.json` | Override schema: `{ spread_id: { text, caption, image } }` |
| `docs/data/authoring_output.json` (first 80 lines) | Top-level schema: `{ spreads: [{ spread_id, text_options, design_specs }] }` |

---

## 7. Summary of Work

1. **Create PHP API backend** (~4 endpoints, flat-file JSON storage)
2. **Add user dropdown** to all 3 page headers
3. **Replace localStorage calls** in all 3 pages with API calls (+ localStorage fallback)
4. **Show multi-user feedback** with usernames in comment panels
5. **Deploy** to Hostinger via MCP upload
6. **Verify** DNS and test the live site

The static JSON data files and images are unchanged — only the user-interaction layer gets a backend.
