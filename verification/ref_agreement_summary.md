# Reference agreement — full suite (DESIGN Amendment 8.1; DECISIONS entry 20 condition)

> **v1 — INCOMPLETE against Amendment 8.1 (author finding, 2026-11-05).** This run compared θ, realised counts, leads, N_out, n* and C_min. It did **not** compare onset steps or the censored/detected/concurrent flags, which 8.1 requires. Equal leads don't imply equal flags (lead 0 can be a miss or concurrent; lead 1,280 can be censored or an onset exactly at the window start), and equal counts don't imply equal onset positions.
> - The harness has been extended (`compare_ref.py`, watch-to-fail test `scripts/tests/test_compare_ref.py`, 10/10).
> - The full run is repeated as v2 into `scripts/outputs/ref_agreement_v2/`.
> - This v1 record is kept as a clean run (all clean runs are committed).

Run on JAE's Windows host, finished 2026-11-05, with `python scripts\suite\run_ref_agreement.py --workers 16` at commit 1fc1f43.
- Pipeline: `analysis/` at 1fc1f43. Reference: `reference/ref_e2.py` 3dfdc9c74591158cb64e003fb55272a0 (amended through Amendment 9 by its original author).
- What is compared for every cell × replicate: N_out, n*, and, per detector, θ (1e-6 relative), the realised onset count and every lead; then C_min (1e-6, same sign).
- Excluded cells: unequal_memory_null (S₁/S₄₀ are not part of the E2 chain; criterion pending S-2) and null_30_50 (pulse height h not yet calibrated).
- Verified on device 2026-11-05: 110 files, each with exactly 200 unique replicates 0–199.

**Result: 22000 comparisons, 0 differ — ALL IDENTICAL.**

| kind | cells | comparisons |
|---|---|---|
| planted_effect | 60 | 12000 |
| regime_span | 20 | 4000 |
| planted_null | 5 | 1000 |
| surge_null | 5 | 1000 |
| surge_effect | 5 | 1000 |
| t3_null | 5 | 1000 |
| decision_flip | 5 | 1000 |
| t3_decision_flip | 5 | 1000 |

## Per-cell manifest (MD5 of each output file)

| cell | kind | φ_y | reps | identical | MD5 |
|---|---|---|---|---|---|
| 0 | planted_effect | 0.5 | 200 | 200 | ad74479bded671c4dc95dde7ca0b3359 |
| 1 | planted_effect | 0.5 | 200 | 200 | ff76c1413f2fccedded64f0b4a7731ef |
| 2 | planted_effect | 0.5 | 200 | 200 | 47d32435b9b7932a13b9e32d656dfce8 |
| 3 | planted_effect | 0.5 | 200 | 200 | 171df6546727124c30cc956040ac7e61 |
| 4 | planted_effect | 0.5 | 200 | 200 | 263948fcbab5ca445e39a7d40dd9abb4 |
| 5 | planted_effect | 0.5 | 200 | 200 | 358ea1d2c1f2afe65ec5f63d3f8f83ad |
| 6 | planted_effect | 0.5 | 200 | 200 | 83f25588036458565fa51325e1c59050 |
| 7 | planted_effect | 0.5 | 200 | 200 | d150ad167f402b9e539fbcaa5a64d059 |
| 8 | planted_effect | 0.5 | 200 | 200 | 635bd0e381247afd9dc315d5a9114a32 |
| 9 | planted_effect | 0.5 | 200 | 200 | 0874508c8288552a21b6f97399b71a45 |
| 10 | planted_effect | 0.5 | 200 | 200 | 8cd1ddede7af77c4423e4bac9030159a |
| 11 | planted_effect | 0.5 | 200 | 200 | b5fc7fb6909355a53b95e041015c1202 |
| 12 | planted_effect | 0.8 | 200 | 200 | fa0a7ccbe113bccb713fd5447a9a658e |
| 13 | planted_effect | 0.8 | 200 | 200 | 5363cb62656b9c1dd62b970a39848b92 |
| 14 | planted_effect | 0.8 | 200 | 200 | c0d64efe67225b93cc064775394aa453 |
| 15 | planted_effect | 0.8 | 200 | 200 | e22faca0a8e8049200d1d029a235d9da |
| 16 | planted_effect | 0.8 | 200 | 200 | 7f88c788b41c5e17b22a4a343077ab64 |
| 17 | planted_effect | 0.8 | 200 | 200 | 8624be25a5c751d4d1c85f403aebb807 |
| 18 | planted_effect | 0.8 | 200 | 200 | d46027aa3d754df1963b304109bdca19 |
| 19 | planted_effect | 0.8 | 200 | 200 | c482ba8743d055b00e889976d4bf8211 |
| 20 | planted_effect | 0.8 | 200 | 200 | 19715c4a47ff99a6176c077b21955512 |
| 21 | planted_effect | 0.8 | 200 | 200 | 072fcacfb80573f883a8c1bcbf9c5047 |
| 22 | planted_effect | 0.8 | 200 | 200 | 3c1a367034ec537196a3a3d355895fb6 |
| 23 | planted_effect | 0.8 | 200 | 200 | afc881caca27fb0ce84de09548e2451a |
| 24 | planted_effect | 0.9 | 200 | 200 | 9c6bbcc9a235df57fc53f80978104d75 |
| 25 | planted_effect | 0.9 | 200 | 200 | 3470f039126b17de121061a3acb9fcab |
| 26 | planted_effect | 0.9 | 200 | 200 | 5a6d82bfb05c3acd56139f87abc658f5 |
| 27 | planted_effect | 0.9 | 200 | 200 | d4f60a36a27c565991aa1235e0e7b1d1 |
| 28 | planted_effect | 0.9 | 200 | 200 | 9450a16af89cfceff7e51ce5b0216dbb |
| 29 | planted_effect | 0.9 | 200 | 200 | dfe555057d669c55d4bfe58d707fb3ee |
| 30 | planted_effect | 0.9 | 200 | 200 | 43f8cfc012f87c06ebda8cf47ab12ae2 |
| 31 | planted_effect | 0.9 | 200 | 200 | b8552772d0394e453cd66bcb9b4766d6 |
| 32 | planted_effect | 0.9 | 200 | 200 | 51c3ae0a3ba06dfb3b191dc3d5dcf5a9 |
| 33 | planted_effect | 0.9 | 200 | 200 | 7905f47261b9a79ed700dc971489d6ac |
| 34 | planted_effect | 0.9 | 200 | 200 | 45ffbcd1dd759419ab1f81cfca117236 |
| 35 | planted_effect | 0.9 | 200 | 200 | 34100f2a3fb9bb8034516d63c041a63a |
| 36 | planted_effect | 0.95 | 200 | 200 | 7065e9f2cabee153014dc2e3e07c2e93 |
| 37 | planted_effect | 0.95 | 200 | 200 | 5255b3abfbdc82f78239fa8ae323f96f |
| 38 | planted_effect | 0.95 | 200 | 200 | ec302f98e979706e1ed1898a41c42bf0 |
| 39 | planted_effect | 0.95 | 200 | 200 | 0de3ee077f1c1799e4b8dff17d3efe33 |
| 40 | planted_effect | 0.95 | 200 | 200 | 73175d024bcb9d16a2f8539142327b4f |
| 41 | planted_effect | 0.95 | 200 | 200 | 28776dfc33b9d98162e33c78d49baf55 |
| 42 | planted_effect | 0.95 | 200 | 200 | 4ebba31fb996067c40bd6a6dfe06acb1 |
| 43 | planted_effect | 0.95 | 200 | 200 | 6a97b6f12b1efda5588e5527a433693c |
| 44 | planted_effect | 0.95 | 200 | 200 | fa93cd518f183ac93214ff1a4993894a |
| 45 | planted_effect | 0.95 | 200 | 200 | dfa1bcc7bd3b45b3fb86eed0817009be |
| 46 | planted_effect | 0.95 | 200 | 200 | 7ee6669ab940197bc3c9441785e5a1aa |
| 47 | planted_effect | 0.95 | 200 | 200 | 6add24ddf3f32e9c1a1b93df0eb3a7c3 |
| 48 | planted_effect | 0.98 | 200 | 200 | bf85e1e3bdfb860db3f5156389f3b227 |
| 49 | planted_effect | 0.98 | 200 | 200 | 457fcdf6fe03441e6d96b563aaf61b1b |
| 50 | planted_effect | 0.98 | 200 | 200 | 5eb87ebb2cec0eb8dd4d143d89c57da2 |
| 51 | planted_effect | 0.98 | 200 | 200 | 693163e9e21b559d6af4212ec855f6b0 |
| 52 | planted_effect | 0.98 | 200 | 200 | c1fd98775249f5a9a93890dc1a4e7673 |
| 53 | planted_effect | 0.98 | 200 | 200 | 3ce67be92b3fec5b2cc163409413f584 |
| 54 | planted_effect | 0.98 | 200 | 200 | 0b5f61c88ee567bac16e08259e43f5f6 |
| 55 | planted_effect | 0.98 | 200 | 200 | 84b89297ff43cfc98ea03cf0bac8e27d |
| 56 | planted_effect | 0.98 | 200 | 200 | 2c40d7efc12a8a733500b9fffeeffc14 |
| 57 | planted_effect | 0.98 | 200 | 200 | 27ceaa73ef89338045e8c1b5b0b367d6 |
| 58 | planted_effect | 0.98 | 200 | 200 | e5e83fdd89d5b9ec5a73bfa0cb4673c4 |
| 59 | planted_effect | 0.98 | 200 | 200 | 3edc773e6594aef8e33ae1cdcd3602c5 |
| 60 | regime_span | 0.5 | 200 | 200 | fec7cd410ae821d9dfc8d867a0815e1f |
| 61 | regime_span | 0.5 | 200 | 200 | b3a9845792303cd564a936bb2b8977a3 |
| 62 | regime_span | 0.5 | 200 | 200 | 52c1caa599cebfb3a7f2265e37c980b0 |
| 63 | regime_span | 0.5 | 200 | 200 | c594152fb2387774d8074de94b83f5d4 |
| 64 | regime_span | 0.8 | 200 | 200 | 532806e64c9fc490224cc8f72ddf7a04 |
| 65 | regime_span | 0.8 | 200 | 200 | f80c91980a3e7d871051298bffb26614 |
| 66 | regime_span | 0.8 | 200 | 200 | 5c5c68196b14d5146d2231fa3514e86e |
| 67 | regime_span | 0.8 | 200 | 200 | 621e18646b2b2408e61e1f421f335aad |
| 68 | regime_span | 0.9 | 200 | 200 | 9fecc5f0884daa98e3f3310fd775dbbd |
| 69 | regime_span | 0.9 | 200 | 200 | ddfe53e8e987aabb2cebe3798c7b72f3 |
| 70 | regime_span | 0.9 | 200 | 200 | ac92a5c846d88a402b8346ab986c11c8 |
| 71 | regime_span | 0.9 | 200 | 200 | 2469c7e5890c0b4693110c795363bf49 |
| 72 | regime_span | 0.95 | 200 | 200 | 98d4728c5da1526835f3bb8a06342861 |
| 73 | regime_span | 0.95 | 200 | 200 | aea7730db1d93d27e10dd61581c26a64 |
| 74 | regime_span | 0.95 | 200 | 200 | 944be13bfcdca54a9a6852e72b585557 |
| 75 | regime_span | 0.95 | 200 | 200 | 6c552ef49bb1db0e24ffc759c8187e17 |
| 76 | regime_span | 0.98 | 200 | 200 | f1d48f18e3df2780aaaae61e1121c050 |
| 77 | regime_span | 0.98 | 200 | 200 | fd7a3b01b0533794955c5afe888af3de |
| 78 | regime_span | 0.98 | 200 | 200 | 7dbb3ba8485bc2328fd6a4f01aae46e8 |
| 79 | regime_span | 0.98 | 200 | 200 | d07a3b6a60b17ea8c2607030fae470e4 |
| 80 | planted_null | 0.5 | 200 | 200 | 211d4e226edfffc8725636fc05baa292 |
| 81 | planted_null | 0.8 | 200 | 200 | d058f9a8b888cfcdd9cf0b92e93ef9de |
| 82 | planted_null | 0.9 | 200 | 200 | a16292b934330ab20d4012e04378222b |
| 83 | planted_null | 0.95 | 200 | 200 | b5c888f805af005dd9b6014a051fbd75 |
| 84 | planted_null | 0.98 | 200 | 200 | 09815a3c992460439e5caad7055d50df |
| 85 | surge_null | 0.5 | 200 | 200 | 1afef6398626163035e1d30a8f39a8aa |
| 86 | surge_effect | 0.5 | 200 | 200 | ce0e38d2de497fde1ed89795dd873c33 |
| 87 | surge_null | 0.8 | 200 | 200 | 1d8093d3112da2747dd96d12e8d5f08e |
| 88 | surge_effect | 0.8 | 200 | 200 | b26dc96322ead5909ce19496b91d6f23 |
| 89 | surge_null | 0.9 | 200 | 200 | 9ab120e8e1b520ed339e4d9faa891a3c |
| 90 | surge_effect | 0.9 | 200 | 200 | de0422ea2fd90d23e641088dc407c180 |
| 91 | surge_null | 0.95 | 200 | 200 | 1a2f9e0590153b3c0b23234107126891 |
| 92 | surge_effect | 0.95 | 200 | 200 | c132d0b188dd99012ac1c736d53cfccb |
| 93 | surge_null | 0.98 | 200 | 200 | 05a06c48a8372056085d48759bf65fd8 |
| 94 | surge_effect | 0.98 | 200 | 200 | ab7c454f96b099efc5073452782d64a6 |
| 95 | t3_null | 0.5 | 200 | 200 | 36958c998fa513c4753c4a4e758ae32a |
| 96 | t3_null | 0.8 | 200 | 200 | 7bac5b238a0576e946bb5c628d85a4b8 |
| 97 | t3_null | 0.9 | 200 | 200 | 471231621107af93ada59e4e934521dc |
| 98 | t3_null | 0.95 | 200 | 200 | a498c22c8164c4175a812a6b69d1ba84 |
| 99 | t3_null | 0.98 | 200 | 200 | 470e71461b08ac05eb68af4771af83c9 |
| 105 | decision_flip | 0.5 | 200 | 200 | 76c916c2ab823a46089c65d9bfafed9e |
| 106 | t3_decision_flip | 0.5 | 200 | 200 | 28a24e8a57146db4963e3e755909b804 |
| 107 | decision_flip | 0.8 | 200 | 200 | cb9fbec4e7ab25605fa2bbec174467c9 |
| 108 | t3_decision_flip | 0.8 | 200 | 200 | bbdc9a9cf50c12d7e7e1a5aa47148171 |
| 109 | decision_flip | 0.9 | 200 | 200 | 77b7ae810729a5fbe8eccb43e71a9075 |
| 110 | t3_decision_flip | 0.9 | 200 | 200 | 20bf7c805d609f127169cc869a8621c2 |
| 111 | decision_flip | 0.95 | 200 | 200 | 911f7b60619d41438086a6c47297a951 |
| 112 | t3_decision_flip | 0.95 | 200 | 200 | 32f3ffe4af3f9312a5c91931d1381998 |
| 113 | decision_flip | 0.98 | 200 | 200 | a523bd8918e29e35676a2add6d7a34d0 |
| 114 | t3_decision_flip | 0.98 | 200 | 200 | ce8519b0637ddde4440d4a39dfe287a6 |
