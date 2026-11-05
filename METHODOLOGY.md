# Methodology

**Scope.** Separately named general-purpose models (including multimodal and open-weights) made generally available through a developer's principal lines, 14 March 2023 to 7 October 2026. Specialised lines (code, maths, speech, image, OCR) and restricted releases are outside scope.

**Dates.** First availability is taken from the vendor's own dated page, API changelog or release notes. Press and third-party trackers were used only to arbitrate between conflicting vendor pages. Announcement-only dates are not used, except where noted (xAI Grok-1.5).

**Strict count.** General-availability launches count at first availability; open-weights releases at the weights date; preview, beta, experimental and gated launches count at their verified GA date, or are not counted if none is verified.

**Verification.** Each row was checked against vendor pages by developer; rows not confirmed are flagged `unv=1` or `conf=low`. Qwen dates were checked against qwen.ai blog headers, GitHub and Hugging Face records and Alibaba Cloud Model Studio and QwenCloud changelogs.

**Known limits.** Prices, context and cutoffs are sparse; GA dates are missing for several developers where the vendor does not state them; 6 rows are lower confidence or unverified (Google 1, OpenAI 1, Qwen (Alibaba) 3, xAI 1).

**Reproducing.** `scripts/` holds the merge and workbook builders; they read intermediate per-developer verification files that are not published here, so they document the method rather than regenerate the data from scratch.
