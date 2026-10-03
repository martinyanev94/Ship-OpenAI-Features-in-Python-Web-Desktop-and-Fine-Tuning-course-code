# Request / response checklist

Fill this from a **live** successful `inspect_response.py` run in your activated venv.

## Request you sent

- [ ] `OPENAI_API_KEY` loaded from the environment (not hardcoded in source)
- [ ] Model id: `gpt-3.5-turbo`
- [ ] Messages: one item with `role` = `user` and fixed primary-colors `content`

## Response fields to confirm

| Field | Value from your run |
| --- | --- |
| `response.model` | _paste here_ |
| `choices[0].message.role` | _expect `assistant`_ |
| `choices[0].message.content` | _paste non-empty reply_ |
| `usage.prompt_tokens` | _paste positive integer_ |
| `usage.completion_tokens` | _paste positive integer_ |
| `usage.total_tokens` | _paste positive integer (prompt + completion)_ |

## Auth failure drill

1. Temporarily set `OPENAI_API_KEY` to `invalid-placeholder`.
2. Run `python inspect_response.py`.
3. Note the symptom (authentication / invalid API key style error):

   > _write what you saw_

4. Restore your real `OPENAI_API_KEY` and rerun until the six labeled lines succeed.

## Decision rule

- Missing or wrong key → fix the environment credential before changing prompts.
- Successful create → UI code should consume `choices[0].message.content`, not the whole `ChatCompletion` object.
- Read `usage.prompt_tokens`, `usage.completion_tokens`, and `usage.total_tokens` so you can tell whether cost grew from a longer prompt or a longer reply.
