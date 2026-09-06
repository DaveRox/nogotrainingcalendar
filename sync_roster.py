"""
NOLA Attendance Tracker — Roster Sync Script
─────────────────────────────────────────────
Run this script (or ask Claude to run it) after making changes
in the Roster Manager sheet of the attendance workbook.

  ADD an agent:  Enter name + class in a new row, set Status = NEW
  REMOVE agent:  Find their row, set Status = REMOVE

Then ask Claude: "sync the roster"
"""

import os
import sys
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

# ── Config ──────────────────────────────────────────────────────────────
WORKBOOK = os.path.join(os.path.dirname(__file__), 'NOLA_Attendance_v3.xlsx')

WEEKLY_SHEETS = [
    'Mar 9', 'March 16', 'Mar 23', 'Mar 30',
    'Apr 6', 'Apr 13', 'Apr 20', 'Apr 27',
    'May 4', 'May 11', 'May 18', 'May 25',
    'Jun 1', 'Jun 8', 'Jun 15', 'Jun 22', 'Jun 29',
]

VALID_CLASSES = {'1P', '2P', '3P', 'PTAS', 'CC'}

# Sessions that apply per class type (None in those cols = N/A)
# PTAS/CC agents have None in Mon AM; all agents have None in other N/A sessions
# We replicate the existing pattern: if a class attends a session, pre-fill ' '
CLASS_SESSIONS = {
    '1P':   [True,  True,  True,  False, True],   # Mon AM, SIE, Wed 9, PTAS, Fri
    '2P':   [True,  True,  True,  False, True],
    '3P':   [True,  True,  True,  False, True],
    'PTAS': [True,  False, False, True,  False],
    'CC':   [True,  False, False, False, True],
}

# ── Styles (match workbook) ──────────────────────────────────────────────
BODY_FONT   = Font(name='Arial', size=10)
CENTER      = Alignment(horizontal='center', vertical='center', wrap_text=True)
LEFT        = Alignment(horizontal='left',   vertical='center')
thin        = Side(style='thin',   color='BFBFBF')
med         = Side(style='medium', color='2E75B6')
BORDER      = Border(left=thin, right=thin, top=thin, bottom=thin)
ALT_FILL    = PatternFill('solid', fgColor='EBF3FB')
GRAY_FILL   = PatternFill('solid', fgColor='D9D9D9')
FILL_ACTIVE = PatternFill('solid', fgColor='C6EFCE')
FONT_ACTIVE = Font(name='Arial', size=10, color='276221')


def load_roster(ws_roster):
    """Read all agents from the Roster sheet. Returns list of (name, cls, status, row)."""
    agents = []
    for r in range(8, ws_roster.max_row + 1):
        name   = ws_roster.cell(r, 1).value
        cls    = ws_roster.cell(r, 2).value
        status = ws_roster.cell(r, 3).value
        if name and str(name).strip():
            agents.append((str(name).strip(), str(cls).strip() if cls else '', str(status).strip() if status else 'Active', r))
    return agents


def get_sheet_agents(ws):
    """Return list of (name, row) from a weekly or master sheet."""
    result = []
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v and str(v).strip():
            result.append((str(v).strip(), r))
    return result


def insert_agent_row(ws, name, cls, after_row, sheet_type='weekly', alt_idx=0):
    """Insert a new agent row at after_row+1 on a weekly or master sheet."""
    insert_at = after_row + 1
    ws.insert_rows(insert_at)

    ws.cell(insert_at, 1).value = name
    ws.cell(insert_at, 2).value = cls

    alt = ALT_FILL if alt_idx % 2 == 1 else PatternFill(fill_type=None)

    if sheet_type == 'weekly':
        sessions = CLASS_SESSIONS.get(cls, [True, True, True, False, True])
        for ci, (col, attends) in enumerate(zip([3, 4, 5, 6, 7], sessions), start=3):
            cell = ws.cell(insert_at, col)
            cell.value     = ' ' if attends else None
            cell.font      = BODY_FONT
            cell.alignment = CENTER
            cell.border    = BORDER if col not in (3, 5) else Border(
                left=med, right=med, top=thin, bottom=thin
            )
            cell.fill = GRAY_FILL if not attends else PatternFill(fill_type=None)

        for c in [1, 2]:
            cell = ws.cell(insert_at, c)
            cell.font      = BODY_FONT
            cell.alignment = LEFT if c == 1 else CENTER
            cell.border    = BORDER
            cell.fill      = alt

        for c in range(8, 13):
            cell = ws.cell(insert_at, c)
            cell.fill      = PatternFill('solid', fgColor='F2F2F2')
            cell.border    = BORDER
            cell.font      = BODY_FONT
            cell.alignment = CENTER

        ws.row_dimensions[insert_at].height = 16

    elif sheet_type == 'master':
        for c in range(1, 11):
            cell = ws.cell(insert_at, c)
            cell.font      = BODY_FONT
            cell.border    = BORDER
            cell.alignment = LEFT if c <= 2 else CENTER
            cell.fill      = alt
        ws.row_dimensions[insert_at].height = 18


def rebuild_master_formulas(ws_master, all_weekly):
    """Rewrite Mon AM and Wed 9 absence formulas for every agent row."""
    for r in range(2, ws_master.max_row + 1):
        if not ws_master.cell(r, 1).value:
            continue
        mon = '+'.join(
            [f'IF(COUNTIF(\'{s}\'!$C:$G,"x")>0,COUNTIF(\'{s}\'!C{r}," "),0)' for s in all_weekly]
        )
        wed = '+'.join(
            [f'IF(COUNTIF(\'{s}\'!$C:$G,"x")>0,COUNTIF(\'{s}\'!E{r}," "),0)' for s in all_weekly]
        )
        ws_master[f'C{r}'] = '=' + mon
        ws_master[f'D{r}'] = '=' + wed
        ws_master[f'E{r}'] = f'=C{r}+D{r}'
        ws_master[f'F{r}'] = (
            f'=IF(E{r}>=3,"Final Notice",'
            f'IF(E{r}>=2,"Warning",'
            f'IF(E{r}>=1,"Alert","OK")))'
        )


def sync(workbook_path=WORKBOOK):
    print(f"\nLoading: {workbook_path}")
    wb = load_workbook(workbook_path)

    ws_roster = wb['Roster']
    ws_master = wb['Master']

    roster = load_roster(ws_roster)

    to_add    = [(n, c, r) for n, c, s, r in roster if s.upper() == 'NEW']
    to_remove = [(n, c, r) for n, c, s, r in roster if s.upper() == 'REMOVE']

    if not to_add and not to_remove:
        print("No changes detected (no rows marked NEW or REMOVE). Nothing to do.")
        return

    print(f"\nTo ADD:    {[n for n,c,r in to_add]}")
    print(f"To REMOVE: {[n for n,c,r in to_remove]}")

    all_sheets = ['Master'] + WEEKLY_SHEETS

    # ── REMOVE agents ─────────────────────────────────────────────────
    for name, cls, _ in to_remove:
        removed_count = 0
        for sh_name in all_sheets:
            if sh_name not in wb.sheetnames:
                continue
            ws = wb[sh_name]
            for agent_name, row in get_sheet_agents(ws):
                if agent_name.lower() == name.lower():
                    ws.delete_rows(row)
                    removed_count += 1
                    break
        print(f"  REMOVED '{name}' from {removed_count} sheets.")

    # ── ADD agents ────────────────────────────────────────────────────
    for name, cls, _ in to_add:
        if cls not in VALID_CLASSES:
            print(f"  WARNING: '{name}' has invalid class '{cls}'. Skipping.")
            continue

        added_count = 0
        for sh_name in all_sheets:
            if sh_name not in wb.sheetnames:
                continue
            ws = wb[sh_name]
            current = get_sheet_agents(ws)
            names_only = [a[0] for a in current]

            if name in names_only:
                print(f"  '{name}' already exists in {sh_name}, skipping.")
                continue

            # Find alphabetical insertion point
            insert_after_row = 1  # default: insert at top of data
            for existing_name, existing_row in current:
                if existing_name.lower() < name.lower():
                    insert_after_row = existing_row
                else:
                    break

            alt_idx = len([n for n, _ in current if n.lower() < name.lower()])

            stype = 'master' if sh_name == 'Master' else 'weekly'
            insert_agent_row(ws, name, cls, insert_after_row, sheet_type=stype, alt_idx=alt_idx)
            added_count += 1

        print(f"  ADDED '{name}' ({cls}) to {added_count} sheets.")

    # ── Rebuild Master formulas (row numbers may have shifted) ────────
    print("\nRebuilding Master formulas...")
    rebuild_master_formulas(ws_master, WEEKLY_SHEETS)

    # ── Update Roster: set processed statuses back to Active ──────────
    for r in range(8, ws_roster.max_row + 1):
        status = ws_roster.cell(r, 3).value
        name   = ws_roster.cell(r, 1).value
        if not name:
            continue
        removed_names = [n.lower() for n, c, _ in to_remove]
        if status and status.upper() == 'NEW':
            ws_roster.cell(r, 3).value = 'Active'
            ws_roster.cell(r, 3).fill  = FILL_ACTIVE
            ws_roster.cell(r, 3).font  = FONT_ACTIVE
        elif status and status.upper() == 'REMOVE':
            # Clear the row since agent is gone
            for c in range(1, 5):
                ws_roster.cell(r, c).value = None

    wb.save(workbook_path)
    print(f"\nDone. Saved: {workbook_path}")
    print("Formula recalculation needed — run: python scripts/recalc.py <workbook>")


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else WORKBOOK
    sync(path)
