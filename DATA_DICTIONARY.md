# Data dictionary

File: `data/ai_model_releases.csv` (UTF-8, one row per model, primary key `id`). Empty means not verified at a vendor source, never zero. Dates are ISO 8601.

| Column | Meaning |
|---|---|
| `dev` | Developer |
| `name` | Model name as the vendor writes it |
| `st` | Stage at launch (ga, open_weights_release, preview, beta, experimental, gated) |
| `counted` | 1 if counted under the strict rule |
| `cd` | Count date (YYYY-MM-DD) |
| `cb` | Which date was used for counting |
| `why` | Reason not counted |
| `ci` | Date used if every stage is counted |
| `an` | Announcement date |
| `fa` | First date the public could use the model |
| `ga` | General-availability date |
| `api` | First date available through the API |
| `wt` | Open-weights publication date |
| `stat` | active, legacy, deprecated or retired |
| `ret` | Vendor retirement date |
| `rep` | Vendor-named successor |
| `ctx` | Context window, tokens |
| `mx` | Maximum output, tokens |
| `ck` | Knowledge cutoff, YYYY-MM |
| `pi` | USD per 1M input tokens |
| `pc` | USD per 1M cached input tokens |
| `po` | USD per 1M output tokens |
| `lic` | Licence |
| `pt` | Total parameters, billions |
| `pa` | Active parameters, billions |
| `ar` | dense or moe |
| `mi` | Input modalities: t text, i image, a audio, v video, pdf |
| `rm` | Reasoning mode |
| `plat` | Platforms (comma separated) |
| `apiid` | API model ID |
| `snap` | Parent model if a variant |
| `src` | Vendor page |
| `card` | Model or system card |
| `conf` | high, medium or low |
| `unv` | 1 if not confirmed against a vendor page |
| `note` | Conflicts and caveats |
| `id` | Stable key developer__slug (primary key) |
