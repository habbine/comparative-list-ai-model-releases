# Comparative list of AI model releases

A source-checked, dated list of **224 general-purpose AI models** from **eight developers**, first made public between **14 March 2023 and 7 October 2026**. Data retrieved **5 November 2026**.

**Files**

- [`data/ai_model_releases.xlsx`](data/ai_model_releases.xlsx): the workbook for reading and filtering (8 sheets).
- [`data/ai_model_releases.csv`](data/ai_model_releases.csv): the same Models table as plain text (UTF-8, one row per model, primary key `model_id`) for scripts and version control. Empty means not verified, never zero; dates are ISO 8601.
- [`docs/index.html`](docs/index.html): the AI model explorer, a self-contained page to pick a developer and choose which information to show. Open it in a browser (after download, or through GitHub Pages if enabled).

## What is in it

| Developer | Models | Counted (strict) | Confidence: high / medium / low |
|---|---:|---:|---:|
| Anthropic | 29 | 27 | 24 / 5 / 0 |
| DeepSeek | 20 | 18 | 17 / 3 / 0 |
| Google | 28 | 23 | 12 / 16 / 0 |
| Meta | 12 | 9 | 9 / 3 / 0 |
| Mistral | 33 | 30 | 19 / 14 / 0 |
| OpenAI | 42 | 37 | 26 / 15 / 1 |
| Qwen (Alibaba) | 43 | 40 | 20 / 20 / 3 |
| xAI | 17 | 13 | 5 / 11 / 1 |
| **Total** | **224** | **197** | **132 / 87 / 5** |

For each model the workbook gives, where a vendor source states it: stage at launch (general availability, preview, beta, experimental, gated, open weights), announcement, first-available, general-availability, API and open-weights dates, status and retirement date, context window, maximum output, knowledge cutoff, list prices per million tokens, licence, parameters and architecture, input modalities, platforms, API model ID, and the vendor page and model card used.

## Sheets

| Sheet | Use |
|---|---|
| Read me | Scope and rules, inside the file |
| Summary | Short view: 11 key columns for each model, linked to Models |
| Models | The data, 37 columns. Filter with the header arrows; alphabetical by developer, then by date |
| Counts | Models per developer and year, computed live from Models; last 12 months against the previous 12; exact binomial p-value; chart of models per quarter |
| Compare versions | First-public dates in four successive versions of the list, with the spread in days and a change flag |
| Not counted | Models in the list but outside the strict count, with the reason |
| Coverage | How many models have each field filled |
| Fields | What each column means and its unit |
| Sources | Every vendor URL used (385), one row per model and source |

## How to use it

1. Open **Models** and filter on the header arrows (for example Developer = OpenAI, Status = active, then sort by Input $ / 1M tokens).
2. Check **Confidence**, **Verified** and **Notes** before relying on a row. Notes give conflicting dates and the one kept.
3. Use **Counts** for totals. It recalculates if you change the Counted column.
4. Follow the link in **Vendor page** to check any value at its source.

## When to use it, and when not

Use it for release timelines, comparisons of vendors' cadence, price and context-window comparisons at launch, and to find the vendor source of a date.

Do not use it as: a live tracker (it is a snapshot of 5 November 2026); a benchmark or quality ranking; a complete list of every model each vendor has released (specialised lines for code, mathematics, speech, image and OCR, and restricted releases, are out of scope); or a source for fields that are blank.

## Counting rules

- **Strict count (197 models):** each model counts once, at its first general-availability date. General-availability launches count at first availability; open-weights releases at the weights date; preview, beta, experimental and gated launches count at their verified general-availability date, or are not counted if none is verified.
- **Inclusive count (224 models):** every model counts at its first date, whatever its stage. Column "Date if any stage counted".
- The two give different totals and different trends. The choice is the user's; both are in the file.

## Method and confidence

- **Dates** are first public availability from the vendor's own dated page, API changelog or release notes. Press and third-party trackers were used only to settle conflicts between vendor pages.
- **Confidence** is high where a vendor page states the facts directly (132 models, 59%), medium where a vendor page supports the date but some detail rests on one source or conflicts with another (87, 39%), and low where the date or stage was not confirmed on a vendor page (5, 2%). Six rows are flagged and should be checked before citing: Gemini 1.0 Ultra (retirement date), GPT-6 Astra Pro, Qwen-Plus, Qwen-Turbo, Qwen3.7-Flash and Grok-1.5.
- **Coverage** is uneven. Of 224 models: vendor page 100%, first available 99%, licence 99%, status 90%, announced 80%, context window 72%, general availability 67%, API date 67%, list input price 48%, retirement date 42%, open-weights date 35%, knowledge cutoff 28%, model card 26%. Blank means not stated at a vendor source or not verified, never zero.
- **Known limits:** prices are list prices from vendor pages and may be tiered or promotional (see Notes); some vendors do not publish general-availability dates; vendor blog headers and page metadata sometimes differ by a day; a few dates come from a single vendor page.

## Known issues

Six rows are not confirmed on a vendor page and should be checked before citing: Gemini 1.0 Ultra (retirement date rests on a forum post quoting the vendor notice), GPT-6 Astra Pro (no separate start date or API ID), Qwen-Plus and Qwen-Turbo (launch date not stated on the vendor blog), Qwen3.7-Flash (two vendor pages give 21 and 25 July 2026; the earlier is kept) and Grok-1.5 (vendor states only that access followed "in the coming days"; the announcement date is used). Models launched as preview, beta, experimental or gated and with no verified general-availability date are listed in the Not counted sheet. Size variants and snapshots are counted as separate models; the `variant_of` column names the parent model so families can be counted instead.

## Checking the CSV

`python3 scripts/check_dataset.py` validates the CSV (unique keys, ISO dates, known stage and confidence codes, source URL on every row, date order, counting consistency) and exits non-zero on any error.

## Updates and corrections

This is a snapshot taken on 5 November 2026 and is not updated automatically. To report an error or a missing source, open a GitHub issue with the model, the field and a vendor URL.

## CSV columns

`model_id`, `developer`, `model`, `stage_at_launch`, `counted_strict`, `count_date`, `count_basis`, `reason_not_counted`, `count_date_any_stage`, `announced`, `first_available`, `general_availability`, `api_available`, `open_weights`, `status`, `retired_on`, `replaced_by`, `context_window_tokens`, `max_output_tokens`, `knowledge_cutoff`, `input_usd_per_1m_tokens`, `cached_input_usd_per_1m_tokens`, `output_usd_per_1m_tokens`, `licence`, `params_total_billions`, `params_active_billions`, `architecture`, `input_modalities`, `reasoning_mode`, `platforms`, `api_model_id`, `variant_of`, `vendor_page`, `model_card`, `confidence`, `unverified`, `notes`

Stage codes: `ga`, `open_weights_release`, `preview`, `beta`, `experimental`, `gated`. Platforms are comma-separated; input modalities are `t` text, `i` image, `a` audio, `v` video, `pdf`. `counted_strict` is 1 or 0. The Fields sheet of the workbook defines every column.

## Versions

Version 4 (5 November 2026) replaces earlier date sets, which remain in the Compare versions sheet.

## Licence

Data: Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE`. Please cite as (or use `CITATION.cff`): Kim, H. E., *Comparative list of AI model releases*, version 4, 5 November 2026.
