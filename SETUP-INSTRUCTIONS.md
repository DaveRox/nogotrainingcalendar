# NYL New Orleans Training Calendar

## Setup Instructions

### 1. Create GitHub Repository
- Go to [github.com/new](https://github.com/new)
- Name: `nogotrainingcalendar`
- Visibility: Public
- **Do NOT** initialize with README
- Click 'Create repository'

### 2. Upload Files
1. Click 'Add file' → 'Upload files'
2. Drag/drop these files from `TARS OUTPUTS` folder:
   - `index.html`
   - `events.json`
   - `admin/config.yml`
   - Your `NOLOGO 2.png` (rename to `NOLOGO2.png`)
3. Click 'Commit changes'

### 3. Connect to Netlify
1. Sign up at [netlify.com](https://netlify.com) (use GitHub login)
2. From dashboard:
   - Click 'Add new site' → 'Import an existing project'
   - Select GitHub → `nogotrainingcalendar`
   - Branch: `main`
   - **Build command: LEAVE BLANK**
   - Click 'Deploy site'

### 4. Configure Domain
1. In Netlify:
   - Site settings → Domain management
   - Add custom domain: `nogotrainingcalendar.com`
2. At your domain registrar:
   ```
   A @ 75.2.60.5
   A www 75.2.60.5
   ```

### 5. Enable Admin Access
1. In Netlify:
   - Identity → Enable Identity
   - Registration: 'Invite only'
2. Invite coworker:
   - Identity → Invite users → `coworker@email.com`

### 6. Verify Setup
- Public site: `nogotrainingcalendar.com`
- Admin panel: `nogotrainingcalendar.com/admin`

> ⚠️ **Critical**: Wait 24 hours for DNS propagation. Test admin login immediately after inviting users.