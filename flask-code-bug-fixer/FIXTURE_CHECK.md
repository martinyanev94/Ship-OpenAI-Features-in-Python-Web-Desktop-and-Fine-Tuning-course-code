# UI fixture check — factorial TypeError

Use this checklist after clicking **Code Fix** with `samples/factorial_type_error.py`
and `samples/factorial_type_error.txt`.

Works for **local** (`http://127.0.0.1:5000/`) and **Azure**
(`https://bugfixer-demo.azurewebsites.net/` — replace the hostname with yours).

## Pass

- [ ] Explanation text area is nonempty
- [ ] Fixed Code text area is nonempty
- [ ] Explanation mentions TypeError and/or string + integer concatenation
- [ ] Fixed Code looks like paste-ready Python (avoids `str + int` with `+`)
- [ ] Empty Code or Error click shows the client guard status message
- [ ] On Azure: site loads over HTTPS and `/health` returns `{"ok": true, ...}`

## Fail (re-run or debug)

- [ ] Either output stays empty after a successful HTTP 200
- [ ] Fixed Code opens with chatty preface instead of source (prompt leakage)
- [ ] Explanation is only a full rewrite with no diagnosis
- [ ] Azure returns missing `OPENAI_API_KEY` — set Application settings, then retry
- [ ] You used the ZeroDivisionError `average([])` sample instead of this fixture
