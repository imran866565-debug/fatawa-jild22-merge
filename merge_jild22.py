#!/usr/bin/env python3
"""Merge Jild 22 tashreeh chunks into jild-22.json.

Re-runnable: reads every jild-22-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, no empty
jawab), writes jild-22.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  12 chunk files (no splits), 187 chunk items, volume_id 42.
  Source export ~/workspace/fatawa-app/content/jild-22.json: 585 unique
  pages pp. 5-692. Gaps (103, nothing invented): pp. 11-110 (100),
  340, 424, 570 — every gap listed in each chunk's manifest
  missing_pages (Jild 17 lesson).

COMBINE RULES (5 cases; parts ordered by min page; sawal from the
FIRST part; jawab = all parts concatenated in page order; pages =
UNION of all parts' pages; notes = all parts' notes):
  masala 123:   CROSS-ID, rename-then-combine. Chunk 04
                'jild22-masala-123' [269-300] (sawal 199, jawab
                40,630) + chunk 05 'jild22-safaih-allujayn' [301-314]
                (empty sawal, jawab 19,551) -> ONE item
                'jild22-masala-123', pages [269-314]. Sawal from
                chunk 04; jawab concatenated. The rename of the tail
                item is effected by the combine itself (the tail id
                is absorbed; the result keeps the head id). (Risala
                صفائح اللجین فی کون التصافح بکفی الیدین ۱۳۰۶ھ; head
                ends mid-discussion at p. 300; tail covers درجہ پنجم
                تا عاشراً and ends "رسالہ صفائح اللجین… ختم شد"
                p. 314.)
  masala 152:   chunk 06 [382-390] + chunk 07 [391-400] -> [382-400].
                Sawal from chunk 06 (4,912); jawab = 6,100 + 13,802.
  masala 186:   RISALA MEGA-COMBINE (4 parts -> 1). Chunk 07
                'jild22-masala-186' [425-440] (sawal 6,002, jawab
                16,207) + chunk 08 'jild22-masala-186' [441-490]
                (empty sawal, jawab 47,638) + chunk 09
                'jild22-masala-186' [491-540] (empty sawal, jawab
                67,863) + chunk 10 'jild22-hawashi-zubda' [541-542]
                (empty sawal, jawab 2,593) -> ONE item
                'jild22-masala-186', pages [425-542] (118 pages).
                Sawal from chunk 07; jawabs concatenated in page
                order. The hawashi-zubda rename is effected by the
                combine itself (the tail id is absorbed; the result
                keeps the head id). (Whole risala الزبدۃ الزکیۃ
                لتحریم سجود التحیۃ ۱۳۳۷ھ is ONE printed mas'ala —
                heading on p. 425, next printed mas'ala is 187 on
                p. 543. The risala itself ends p. 537 "رسالہ ختم شد";
                pp. 538-542 are its Arabic hawashi appendix,
                summarised only per the printed note.)
  masala 205-208: chunk 10 [580-590] + chunk 11 [591-592] -> [580-592].
                Sawal from chunk 10 (428); jawab = 10,217 + 2,683.
  masala 227:   chunk 11 [607-640] + chunk 12 [641-677] -> [607-677].
                Sawal from chunk 11 (3,625); jawab = 40,275 + 8,764.
                (Whole risala لمعۃ الضحی فی اعفاء اللحی ۱۳۱۵ھ is ONE
                mas'ala; risala closes p. 677 with its count: 18
                آیتیں، 72 حدیثیں، 60 ارشادات علماء = 150 نصوص,
                completed Friday غرہ رجب 1305ھ.)
After all 5 combines: 187 - 7 = 180 items covering 585 unique pages.

RENAMES: none applied in the chunk files — printed numbering runs
cleanly 1-241 with no print-error numbers found in this volume. The
ONLY renames are the two merge-time ones inside combines 1 and 3
above ('jild22-safaih-allujayn' -> 'jild22-masala-123';
'jild22-hawashi-zubda' -> 'jild22-masala-186'), both effected by the
combines themselves (the tail ids are absorbed; the results keep the
head ids). Do NOT globally normalise bare ids.

SORT: merged items are sorted by start_page for the final file.

DO-NOT-COMBINES: masala-221-226 (folded into the single combined
heading "مسئلہ ۲۲۱ و ۲۲۶" p. 605, six sub-questions — one item
'jild22-masala-221-226' [605-606]; nothing is missing from the
sequence); masala-72-87 (the whole 16-question risala مروج النجاء
لخروج النساء ۱۳۱۶ھ, pp. 221-233 — already a single item, no combine
needed); masail 187-201 (pp. 543-569) are separate items in lesson
205 — NOT part of the masala-186 mega-combine; masail 124-139 are
separate items after risala صفائح اللجین; masail 144-185 are
standalone fatawa after risala ابرالمقال ends at masala-143;
masail 228-241 are separate items after risala لمعۃ الضحی. Shared
pages by design: p. 258 (masala-121/122), p. 314 (risala tail /
masala-124), and other boundary pages where items meet. Page union
must still be exactly 585. p. 424 gap: masala-185 ends p. 423, so
risala 204's closing material, if any, lies on the missing page and
is not covered (noted in masala-185's notes). Lesson id 189 is
absent from the volume's lesson sequence (187, 188, 190…) — not a
content gap; pages are continuous. Volume ends p. 692 with the
publisher's note ('jild22-khatima'): "جلد ۲۲ داڑھی وحلق وقصر وختنہ
و حجامت کے بیان پر ختم ہوگئی۔ جلد ۲۳ ان شاء اللہ نماز وطہارت کے
عنوان سے شروع ہوگی۔" — followed by a dangling incomplete sentence
("حدیث میں آیا ہے اور ایک مرفوع حدیث میں ہے کہ") flagged in the
khatima item's notes. PUA-garbled Quran pages: 5 — p. 399 (1 U+F020),
p. 561 (1 U+F06C), p. 601 (1), p. 618 (7), p. 620 (1). Plus U+FFFD
chars on pp. 609, 619, 625, 638 and garbled words on pp. 114, 132,
347, 368, 379. All flagged in item notes only, never reconstructed.

EMPTY FIELDS: ZERO empty jawabs among all 187 chunk items. After
merging, the only empty sawals are pesh-lafz and khatima (by design;
their notes explain).
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild22-masala-123': [
        ('id', 'jild22-masala-123'),
        ('id', 'jild22-safaih-allujayn'),
    ],
    'jild22-masala-152': [
        ('id', 'jild22-masala-152'),
    ],
    'jild22-masala-186': [
        ('id', 'jild22-masala-186'),
        ('id', 'jild22-hawashi-zubda'),
    ],
    'jild22-masala-205-208': [
        ('id', 'jild22-masala-205-208'),
    ],
    'jild22-masala-227': [
        ('id', 'jild22-masala-227'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part).
# All 5 combines take the sawal from the first part, so no overrides.
SAWAL_RULES = {}

# No renames to apply as a separate step — there are no applied-in-chunk
# renames in this volume, and the two merge-time renames (safaih-allujayn
# and hawashi-zubda) are effected by the cross-id combines themselves
# (the tail ids are absorbed; the results keep the head ids).
# Kept empty deliberately.
RENAMES = {}

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild22-masala-123': list(range(269, 315)),
    'jild22-masala-152': list(range(382, 401)),
    'jild22-masala-186': list(range(425, 543)),
    'jild22-masala-205-208': list(range(580, 593)),
    'jild22-masala-227': list(range(607, 678)),
}

# Expected sawal/jawab char counts for every combined item.
# masala-123 jawab: 40630 + 19551 = 60181
# masala-152 jawab: 6100 + 13802 = 19902
# masala-186 jawab: 16207 + 47638 + 67863 + 2593 = 134301
# masala-205-208 jawab: 10217 + 2683 = 12900
# masala-227 jawab: 40275 + 8764 = 49039
EXPECTED_COMBINED_TEXT = {
    'jild22-masala-123': (199, 60181),
    'jild22-masala-152': (4912, 19902),
    'jild22-masala-186': (6002, 134301),
    'jild22-masala-205-208': (428, 12900),
    'jild22-masala-227': (3625, 49039),
}

# The only ids that may be absorbed by a combine (must be gone after).
ABSORBED = ['jild22-safaih-allujayn', 'jild22-hawashi-zubda']

# The only items allowed to keep an empty sawal after merging.
EMPTY_SAWAL_ALLOWED = {'jild22-pesh-lafz', 'jild22-khatima'}


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 42,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 187, f'expected 187 chunk items, got {len(all_items)}'
    # COMBINE the 5 cases (one mas'ala split across chunks).
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"]} != expected {EXPECTED_COMBINED_PAGES[result_id]}'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAMES: none to apply as a separate step (both merge-time renames
    # were effected by the cross-id combines above).
    for old_id, new_id in RENAMES.items():
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items if it['id'] == old_id]
        assert len(hits) == 1, f'rename source {old_id}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone.
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    print(f'absorbed ids gone: {ABSORBED}')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert not empty, f'EMPTY JAWAB: {empty}'
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {sorted(empty_sawal)}')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the 585
    # unique pages directly, not against a range-minus-gaps computation.
    assert len(pages) == 585, f'expected 585 unique pages, got {len(pages)}'
    assert min(pages) == 5 and max(pages) == 692, \
        f'page span {min(pages)}-{max(pages)} != 5-692'
    # Secondary cross-check: manifest ranges minus listed gap pages.
    expected = set()
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            expected.update(range(entry['start_page'], entry['end_page'] + 1))
            expected.difference_update(entry['missing_pages'])
    missing_covered = expected - pages
    extra = pages - expected
    print(f'total items: {len(all_items)} | pages covered: {len(pages)} | expected (manifest): {len(expected)}')
    print(f'uncovered expected pages: {sorted(missing_covered)}')
    print(f'extra pages (outside merged chunks): {sorted(extra)}')
    assert not missing_covered, 'pages missing from merged chunks!'
    assert not extra, 'pages outside merged chunks!'
    assert len(all_items) == 180, f'expected 180 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-22.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild22.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-22.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild22.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
