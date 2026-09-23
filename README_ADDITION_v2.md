## Update: Independent Validation and Additional Baseline (Section 6.7, extended Table 6)

The following files support the independent validation on a second, separately
collected corpus, and the additional MuRIL baseline, added in this revision.

### `data/`
| File | Contents |
|---|---|
| `twitter_validation_corpus_v1.csv` | 1,134 posts, text-free, six indicator labels (final, post-adjudication) plus keyword provenance |
| `twitter_validation_iaa_subset_v1.csv` | The 199-post double-annotated reliability subset: both annotators' original labels and the final adjudicated gold label, per indicator |
| `twitter_validation_adjudication_record.csv` | The 31 disagreement cells (2.6% of decisions), original labels from both annotators, and the independent third-annotator resolution |

### `agreement/`
| File | Contents |
|---|---|
| `twitter_validation_iaa.csv` | Per-indicator Krippendorff's α (Table 12) |
| `twitter_coverage_gap_tfidf.csv` | Coverage-gap replication, character n-gram detectors (Table 13) |
| `twitter_coverage_gap_muril.csv` | Same replication with MuRIL detectors (Section 6.7) |
| `muril_test_fold_results.csv` | MuRIL AUC-PR on the original RU-RAD-6 test fold, n = 227 (extends Table 6) |

### `code/`
| File | Contents |
|---|---|
| `06_muril_baselines.py` | Fine-tunes MuRIL as the hate-speech proxy and as five dedicated per-indicator detectors, with inverse-frequency class weighting; evaluates on both the original test fold and the independent Twitter corpus |
| `07_twitter_validation_mining.py` | High-recall keyword mining logic used to build the Twitter candidate pool, same method as `01_build_pool.py`/`02_active_learning_mining.py` applied to the new source |

### Note on source text

As with the original corpus, source post text for the Twitter validation corpus
is not redistributed, in line with the platform terms of the dataset it was
drawn from. The released files above are sufficient to reproduce every number
reported in Section 6.7 and the extended Table 6. If a public, citable source
for the underlying Twitter dataset exists, add its citation and a rehydration
note here before final release, following the pattern of `code/rehydrate.py`
for the original corpus.
