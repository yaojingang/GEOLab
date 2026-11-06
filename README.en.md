# GEOLab

[简体中文](./README.md) | English

> **Open empirical resources for studying how generative search selects sources, absorbs content, and surfaces entities.**

GEOLab is a research library for GEO / AEO / AI Search papers, datasets, experimental reports, white papers, and research articles. Its current resources cover two empirical research tracks: cross-platform citation experiments and Chinese-language generative search. The repository includes analysis scripts, data warehouses, visual reports, a searchable paper catalog, and an online GEO knowledge assessment.

Simplified Chinese is the default documentation language. This page provides an English overview; most linked reports and collection guides are in Chinese.

`Question → Search triggering → Source selection → Content absorption → Entity exposure → Platform and interface differences`

## Resource directories

| Directory | Contents |
| --- | --- |
| [`01-experiments/`](./01-experiments/) | Cross-platform experiments, analysis scripts, and research reports |
| [`02-papers/`](./02-papers/) | GEO / AEO / AI Search papers and a topic-based catalog |
| [`03-datasets/`](./03-datasets/) | CN-GEO citation data, documentation, and visual analysis |
| [`04-whitepapers/`](./04-whitepapers/) | Domestic GEO White, Red, and Blue Books in HTML and PDF, industry guides, and measurement reports |
| [`05-articles/`](./05-articles/) | Research articles supported by data, methods, or traceable sources |

The domestic GEO White, Red, and Blue Books are available as complete HTML and PDF files. The research article directory is ready for its first entries. Follow each directory's README when adding materials, including the source, date, topic, and file link.

## Domestic GEO White, Red, and Blue Books

Written by Yao Jingang and Xiangyang Qiaomu. This collection contains the November 6, 2026 exports, totaling 618 pages. All three books are in Chinese.

| Book | Topic | Pages | Read online | PDF |
| --- | --- | ---: | --- | --- |
| Domestic GEO White Book | Brand growth in the AI search era | 245 | [Read HTML](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-white.html) | [Download PDF](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-white.pdf) |
| GEO Red Book | Ethical boundaries, manipulation risks, and governance | 204 | [Read HTML](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-red.html) | [Download PDF](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-red.pdf) |
| GEO Blue Book | Evaluating cooperation between enterprises and GEO service providers | 169 | [Read HTML](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-blue.html) | [Download PDF](https://yaojingang.github.io/GEOLab/04-whitepapers/domestic/geo-blue.pdf) |

[Open the book catalog](https://yaojingang.github.io/GEOLab/04-whitepapers/) · [Sources, versions, and checksums](./04-whitepapers/README.md)

The online site serves the complete books and downloads; the lightweight offline Viewer links to the online catalog. PDFs retain their original bytes. HTML navigation and paper-source links are adapted for this collection.

## Install with an AI client

Send the following request to an AI client that has network access and permission to manage local files:

> Install the lightweight GEOLab Viewer and open it:
> https://github.com/yaojingang/GEOLab

The client downloads the version-pinned `v0.1.0` Viewer, verifies its SHA-256 checksum, extracts it, and opens `index.html`. The Viewer includes self-contained research reports and a searchable paper catalog, with an uncompressed size limit of 15 MiB. It runs without Git, Python, Node, or Docker. Paper PDFs and the complete datasets remain available through online links.

The current `release_status` in `deploy/manifest.json` is `released`. The installers use fixed Release asset URLs for `v0.1.0`.

| Request | Result |
| --- | --- |
| "Install and open GEOLab" | Install the lightweight Viewer and open it in the default browser |
| "Deploy the GEOLab Viewer to my GitHub Pages" | Preserve license and attribution files, confirm the target repository and public visibility, then run the Pages publishing workflow |
| "Download the complete data and prepare an analysis environment" | Explain the approximate 641 MiB size, clone the repository, and configure Python 3.11 and `uv` |

Web-based chat clients usually cannot manage local files. Use the [online homepage](https://yaojingang.github.io/GEOLab/) for browsing. Local AI clients should follow the installation contract in [`AGENTS.md`](./AGENTS.md) and [`deploy/manifest.json`](./deploy/manifest.json).

| Research resource | Current scale |
| --- | ---: |
| CN-GEO raw citation records | 214,119 |
| Chinese AI platform and interface codes | 12 |
| Cross-platform experimental prompts | 602 |
| GEO / AEO / AI Search paper index | 122 entries across 18 topics; 65 PDFs in the repository |
| Online GEO knowledge assessment | 30 questions, 100 points, six diagnostic dimensions |

The paper library added 16 entries on October 25, 2026: 11 recent papers and five previously omitted papers. Sources, versions, licenses, and reading recommendations are documented in the [batch update notes](./02-papers/00_资料说明/2026-10-25_GEO论文更新记录.md).

[Take the GEO assessment](https://ai.laoyao.cn/geo/) · [Read the CN-GEO analysis](https://yaojingang.github.io/GEOLab/03-datasets/reports/final/CN-GEO_%E5%A4%9A%E7%BB%B4%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A.html) · [Read the three-minute experimental summary](./01-experiments/QUICK_REPORT.md) · [Browse the paper catalog](https://yaojingang.github.io/GEOLab/02-papers/) · [Open the homepage](https://yaojingang.github.io/GEOLab/)


## Interactive paper learning map

[Open the learning map](https://yaojingang.github.io/GEOLab/02-papers/interactive-guides/) · [Page inventory and source](./02-papers/interactive-guides/)

The map indexes 122 papers and provides 121 interactive courses, with 2,783 whiteboard pages across 18 topics and five learning paths. Courses include plain and professional modes, speaker notes, quizzes and local learning progress. One entry currently contains bibliographic information only.

## Research questions

Visibility in AI search involves several stages. Content can enter the retrieval candidate set, appear in a citation list, contribute to an answer, or influence how brands and entities are presented. Two empirical studies in this repository examine that process.

- [`01-experiments/`](./01-experiments/) studies how ChatGPT, Google AI Overview / Gemini, and Perplexity trigger searches, select sources, and absorb page content.
- [`03-datasets/`](./03-datasets/) organizes Chinese AI citation records and provides queryable data and reports on source composition, page features, entity exposure, and Web / App differences.
- [`02-papers/`](./02-papers/) provides supporting literature on GEO methods, measurement, empirical AI search research, manipulation risks, Agentic Search, and RAG.
- [`geo-assessment/`](./geo-assessment/) turns findings from the papers, cross-platform experiments, and CN-GEO data into 30 scenario-based questions. The assessment is intended for GEO beginners, focuses mainly on applications in China, and produces a report across six dimensions.

## Three research findings

**Citation breadth and absorption depth require separate measurements.** In the cross-platform experiment, Perplexity and Google cite more sources on average. ChatGPT cites fewer sources and shows higher average citation impact among successfully fetched pages. See [From Citation Selection to Citation Absorption](https://arxiv.org/abs/2604.25707) for the full definitions and measurement scope.

**Content relevance, structure, and evidence density are associated with absorption depth.** High-impact pages tend to be longer and more clearly segmented, with more definitions, numbers, comparisons, and procedural steps. A Q&A format alone showed no absorption advantage. These findings come from descriptive statistics and correlation analysis on a static sample.

**Web and App interfaces of the same product need separate analysis.** The Chinese-language generative search study finds systematic differences in source sets across interfaces of the same platform. Interface type affects cross-platform comparisons. See [What Do Chinese-Language Generative Search Engines Cite and Surface?](https://arxiv.org/abs/2607.15771) for the full results.

## Choose a starting point

| Goal | Suggested resource |
| --- | --- |
| Understand the research findings | [CN-GEO online analysis](https://yaojingang.github.io/GEOLab/03-datasets/reports/final/CN-GEO_%E5%A4%9A%E7%BB%B4%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A.html) · [Cross-platform experimental summary](./01-experiments/QUICK_REPORT.md) |
| Use the data or extend the analysis | [CN-GEO dataset overview](./03-datasets/) · [Guide to the cleaned data](./03-datasets/data/清洗后数据使用说明.md) |
| Read papers or cite the research | [Two empirical research tracks](#two-empirical-research-tracks) · [122-entry catalog](https://yaojingang.github.io/GEOLab/02-papers/) |
| Read the domestic GEO White, Red, and Blue Books | [Online reading and PDF downloads](https://yaojingang.github.io/GEOLab/04-whitepapers/) · [Sources and versions](./04-whitepapers/) |
| Read research articles and practical analyses | [Research article directory and collection guide](./05-articles/) |
| Review experiments and processing methods | [Cross-platform pipeline](./01-experiments/03-pipeline/) · [CN-GEO build scripts](./03-datasets/scripts/) |
| Assess your understanding of GEO | [Online assessment](https://ai.laoyao.cn/geo/) · [Source code and local setup](./geo-assessment/) |

Use GitHub Pages to read the findings without cloning the complete repository. The README files in the two research directories explain how to analyze the data and reproduce the calculations.

## Two empirical research tracks

### Cross-platform citation selection and absorption

The experiment covers `602` controlled prompts, `21,143` valid search-layer citations, and `23,745` citation-level feature records. It extracts `72` features from `18,151` successfully fetched pages.

The study distinguishes two observable outcomes:

- **Citation selection:** whether a platform triggers search and which sources enter the citation list.
- **Citation absorption:** how a cited page contributes to the final answer through its language, evidence, structure, and facts.

Associated paper:

> Zhang Kai, He Xinyue, Yao Jingang. [From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms](https://arxiv.org/abs/2604.25707). arXiv:2604.25707, 2026.

Materials include [prompts and data](./01-experiments/), the [full Markdown report](./01-experiments/04-repet/final_report.md), and the [online HTML report](https://yaojingang.github.io/GEOLab/01-experiments/04-repet/final_report.html).

### Chinese-language generative search and CN-GEO

The current CN-GEO release contains `214,119` raw citation records, `64` JSONL shards, `9,878` canonical sources, and `107,659` canonical pages. The repository also provides standard Parquet tables, a self-contained DuckDB database, page features, analytical data marts, quality reports, and visual reports.

Associated paper:

> Tao Zhen, Yue Liu, Gege Zhang, Yixuan Niu. [What Do Chinese-Language Generative Search Engines Cite and Surface? A Large-Scale Empirical Study](https://arxiv.org/abs/2607.15771). arXiv:2607.15771, 2026.

The paper analyzes eight Web / App interfaces across four Chinese large language model products, focusing on citation behavior, entity exposure, and consistency across interfaces.

## Paper library

The library indexes 122 entries across 18 topics, with 121 interactive courses and one bibliography-only entry. The repository retains 65 existing PDFs; additional reading copies use original-source links. Topics include GEO foundations, optimization methods, measurement, empirical AI search research, AEO theory, risks and manipulation, vertical and multimodal applications, Agentic Search, RAG, and search evaluation and governance.

- [Online search and filtering](https://yaojingang.github.io/GEOLab/02-papers/)
- [Complete paper list](./02-papers/README.md)
- [Sources, checksums, and curation notes](./02-papers/00_资料说明/)

## Sources, citation, and limitations

| Resource | Source and the repository's role |
| --- | --- |
| Cross-platform experiments | This repository stores the experimental prompts, data, pipelines, and reports, and provides public data and analysis for arXiv:2604.25707. |
| CN-GEO | Based on [WENDAOstudy/cn-geo-citation-dataset](https://github.com/WENDAOstudy/cn-geo-citation-dataset), licensed under [CC BY 4.0](https://github.com/WENDAOstudy/cn-geo-citation-dataset/blob/main/LICENSE.md), with additional cleaning, querying, and visual analysis. |
| Paper PDFs | Copyright belongs to the original authors or publishers. The repository provides topic-based organization, source links, file lists, and checksums. |

When using the data, account for these limitations:

- The cross-platform experiment is a static research snapshot. A consistent collection timestamp is currently unavailable for each record.
- The CN-GEO raw layer lacks complete answers, answer batches, model versions, and collection times. Source coverage and cross-platform agreement can be studied directly. Trends, sentiment, strict citation rankings, and brand recommendation rates require additional answer-level data.
- The papers, original datasets, and cleaned repository use their own sample definitions and processing conventions. Cite figures using the definitions in the relevant paper or data version.
- Licensing is scoped by material: code and automation use MIT; original reports, documentation, visualizations, and catalog metadata use CC BY 4.0. Paper PDFs, source datasets, and other third-party materials retain their original licenses.

See the [CN-GEO dataset documentation](./03-datasets/data/数据集中文说明.md) and [data quality report](./03-datasets/data/quality/release_date=2026-07-14/quality_report.md) for the full limitations and validation results.

## Publish the lightweight Viewer

Maintainers can build and verify the package locally:

```bash
python3 scripts/build_viewer.py --package
python3 scripts/verify_distribution.py
```

Pushing to `main` runs [`publish.yml`](./.github/workflows/publish.yml), which deploys the lightweight Viewer to GitHub Pages. Pushing a `v*` tag matching `distribution_version` in `deploy/manifest.json` runs the same workflow to publish the Viewer ZIP, SHA-256 checksum, manifest, and both installers.

To prepare the next version, first set `release_status` to `pending`. Update `distribution_version`, the fixed installer URLs, and the version references in the README files together. Set the status to `released` in the release commit, complete verification, and create the matching version tag. The installers and manifest use version-pinned Release URLs to prevent version drift between `main` and `latest` during publication.

When enabling workflow-based deployment for the first time, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. See [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) for the third-party material boundaries of the package.

Code, installers, workflows, and the bundled skill use [MIT](./LICENSE-CODE). Original reports, documentation, visualizations, and catalog metadata use [CC BY 4.0](./LICENSE-CONTENT). You may copy, modify, and publicly deploy the Viewer while preserving [`LICENSE`](./LICENSE), both scoped license files, [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md), and attribution, and identifying any changes. Paper PDFs, source datasets, and other third-party materials retain their original terms.

## Follow updates and contribute

The repository will continue updating its papers, datasets, and analysis reports, and adding white papers and research articles. **Star** the project to bookmark it, or use **Watch** to follow commits and discussions.

Use [Issues](https://github.com/yaojingang/GEOLab/issues) to submit:

- Questions about data fields, cleaning rules, or report definitions.
- Reproducible analyses and proposed corrections.
- GEO / AEO / AI Search papers, datasets, white papers, or research articles worth adding.
