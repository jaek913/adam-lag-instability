# Vendored reference implementations (test-only)

Used only by the D.5 suite probes (DESIGN Amendment 5.3 (iii)–(iv)) to check that `analysis/ops.py` reproduces each tool's own code. They are not imported by any analysis script.

| dir | source | file | SHA-256 | licence |
|---|---|---|---|---|
| zclip_1_0_0 | PyPI `zclip` 1.0.0 sdist (SHA-256 8fd6098e4b7ba81884c2493b187cc87d527e2be5478e2c8d4d77ab85318e622f) | zclip.py | c28177c4fd32a32d63668cda49f76c9274d57858c1d6a9fecb7c511e50418ad8 | Apache-2.0 (LICENSE, 43070e2d…) |
| trainscope_0651b25 | github.com/kaelvalen/trainscope @ 0651b25ea4817b7b04149f2532fb0f346f510cbe | trainscope/core/detectors/changepoint.py | 8c2a544a79e2abada321f53644f3416dd9ab1ebdfbc550c5985822426535e692 | MIT (LICENSE, e7cf2c7d…) |
| trainscope_0651b25 | same commit | trainscope/core/detectors/base.py | da90310f334cf1390c58e860b94929918b742efe2479981ff44d7772b57b8adb | MIT |

The files are unmodified copies. The probes stub `torch` (ZClip's import-time dependency; the arithmetic compared is pure Python) and the trainscope base-class import path.
