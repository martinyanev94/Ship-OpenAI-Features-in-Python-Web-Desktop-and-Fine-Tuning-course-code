# Parameter decision note

## Use case

Constrained bug-fixer: explain a factorial TypeError and provide corrected Python code.

## Controlled input

The model and messages were held constant. Record the model ID and date.

## Observations

| Profile | Temperature | max_tokens | Complete explanation and fix? | Finish reason | Token usage |
|---|---:|---:|---|---|---|
| temperature_low | 0.2 | 180 | `<observation>` | `<observation>` | `<prompt/completion/total>` |
| temperature_high | 0.8 | 180 | `<observation>` | `<observation>` | `<prompt/completion/total>` |
| ceiling_short | 0.2 | 180 | `<observation>` | `<observation>` | `<prompt/completion/total>` |
| ceiling_roomy | 0.2 | 320 | `<observation>` | `<observation>` | `<prompt/completion/total>` |

## Recommendation

Choose `<profile>` because `<tie the observed completeness and usage to the app constraint>`.

## Revisit condition

Re-test if `<the prompt, model, response limit, or required output changes>`.
