# AI model releases

A dated, source-checked list of 224 general-purpose AI models from eight developers (Anthropic, DeepSeek, Google, Meta, Mistral, OpenAI, Qwen, xAI), 14 March 2023 to 7 October 2026. Retrieved 5 November 2026.

- `data/ai_model_releases.csv`: the master table, one row per model, 37 columns, a vendor source URL on each row.
- `data/ai_model_releases.xlsx`: the same data for people, with filters, per-year counts, a comparison of versions v1 to v4, the models not counted, a coverage sheet and every source.
- `docs/index.html`: a page to pick a developer and choose which information to show.
- `DATA_DICTIONARY.md`, `datapackage.json`: schema. `METHODOLOGY.md`: rules.

## Counting
Strict rule: each model counts once, at its first date of general availability (197 of 224 models). The inclusive count uses first availability whatever the stage (224). The choice changes the totals, so both are in the data.

## Caveats
Fields are filled only where a vendor source states them (see the Coverage sheet). Rows with `unv=1` or `conf=low` were not confirmed against a vendor page. Dates are first public availability, which can differ from announcement dates in press and trackers; where vendor pages disagree, the `note` column gives both dates.

## Licence and citation
Data: CC BY 4.0 (to be confirmed by the author). See `CITATION.cff`.
