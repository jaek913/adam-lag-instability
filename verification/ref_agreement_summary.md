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

## v2 — COMPLETE against Amendment 8.1 (2026-11-06)

Run on JAE's Windows host with `python scripts\suite\run_ref_agreement.py --workers 16` at commit aad6cf7. analysis/, scripts/suite/ and reference/ had no uncommitted changes against HEAD, and HEAD = origin/main.
- What is compared: N_out, n*; per detector θ (1e-6 relative), realised count, **onset steps**, every lead with its **censored/detected/concurrent flags**; C_min (1e-6, same sign).
- The harness's watch-to-fail test is `scripts/tests/test_compare_ref.py`, 10/10.
- Verified on device: 110 files, each with exactly the 200 replicates 0–199.

**Result: 22000 comparisons, 0 differ — ALL IDENTICAL.** This satisfies the Amendment 8.1 oracle for the 110 E2-chain cells. The unequal-memory cells are pending S-2; the null_30_50 cells are pending calibration of h.

| cell | kind | φ_y | reps | identical | MD5 |
|---|---|---|---|---|---|
| 0 | planted_effect | 0.5 | 200 | 200 | c40fc1a1315de28e9c5f9a2436f7bd0f |
| 1 | planted_effect | 0.5 | 200 | 200 | 779ad70227df70f2ea85452b3a3b5263 |
| 2 | planted_effect | 0.5 | 200 | 200 | b392e76ffb1866793072eef530b2579d |
| 3 | planted_effect | 0.5 | 200 | 200 | 0314d06d4690a74844529342d6ccde76 |
| 4 | planted_effect | 0.5 | 200 | 200 | 0a8987de20b6c103edd7fb9187cf5a7b |
| 5 | planted_effect | 0.5 | 200 | 200 | 48ddf85168a71286c9276c248c2361a2 |
| 6 | planted_effect | 0.5 | 200 | 200 | 5908c0183a0c7dba1a7ae13a2e82d1b9 |
| 7 | planted_effect | 0.5 | 200 | 200 | 44b073cbc4d5f965d01d1261dbc843fe |
| 8 | planted_effect | 0.5 | 200 | 200 | 3904b8013171aa27b27a8d5a2d4d180c |
| 9 | planted_effect | 0.5 | 200 | 200 | 7d1b666996d7194e7043d8048976d639 |
| 10 | planted_effect | 0.5 | 200 | 200 | 68ae81d41d01d1094ee98dfbd71e9c44 |
| 11 | planted_effect | 0.5 | 200 | 200 | 739f4534dfe334531b04e210c4ec7114 |
| 12 | planted_effect | 0.8 | 200 | 200 | bbea334cc0ce7c8cd14a01adc5f7f8ee |
| 13 | planted_effect | 0.8 | 200 | 200 | 81487b9f700cebeff6b40ebb73c2b451 |
| 14 | planted_effect | 0.8 | 200 | 200 | 5c46a6c81fa881d008eb275e8c0deea6 |
| 15 | planted_effect | 0.8 | 200 | 200 | 2ffa759e5d653a011549d40fd7dd69ed |
| 16 | planted_effect | 0.8 | 200 | 200 | df3e527e2c3e1f30eae7e139744caa13 |
| 17 | planted_effect | 0.8 | 200 | 200 | 3201aa73ed3a071cd88571c582b624a5 |
| 18 | planted_effect | 0.8 | 200 | 200 | f7e58b2d9743eff443d7ba3f2206a058 |
| 19 | planted_effect | 0.8 | 200 | 200 | e4dfb8866ba34a37160f2081ac90a0b6 |
| 20 | planted_effect | 0.8 | 200 | 200 | dba54cfa4cc68f74059513769723c5b7 |
| 21 | planted_effect | 0.8 | 200 | 200 | edc1272199b77624eeef622249be3611 |
| 22 | planted_effect | 0.8 | 200 | 200 | 841cf0e11f06d70302d26d23d135bf1a |
| 23 | planted_effect | 0.8 | 200 | 200 | 7dfc4083a5c808946c16e5e287e1c746 |
| 24 | planted_effect | 0.9 | 200 | 200 | 52d6796d6e07f140c5a76917f9199166 |
| 25 | planted_effect | 0.9 | 200 | 200 | 0636c34ae050144304f78df376feb9ff |
| 26 | planted_effect | 0.9 | 200 | 200 | 2802be99a1961a070725234a663d6413 |
| 27 | planted_effect | 0.9 | 200 | 200 | fe7e3cf20c1c91f3ec7fa1d73715dbf6 |
| 28 | planted_effect | 0.9 | 200 | 200 | 830ebd4edd50fac684afff584df6eba3 |
| 29 | planted_effect | 0.9 | 200 | 200 | 3a01b2c00960a4545f188d3c8db4b39b |
| 30 | planted_effect | 0.9 | 200 | 200 | c759882566586c593e61c13277c2f181 |
| 31 | planted_effect | 0.9 | 200 | 200 | bd8010bf477a21e7c4c652436fa61953 |
| 32 | planted_effect | 0.9 | 200 | 200 | 1f6777f61c4df986a7b1fe1e18c5526d |
| 33 | planted_effect | 0.9 | 200 | 200 | 1fdc641e8365778fa0b0bca4e4971084 |
| 34 | planted_effect | 0.9 | 200 | 200 | 0aa1e1d53edf8f5bbaed1c669ca3cea5 |
| 35 | planted_effect | 0.9 | 200 | 200 | 9e0326c0aac4f77c35da01966d121264 |
| 36 | planted_effect | 0.95 | 200 | 200 | ce4342cb87f66de4aed31d54c47343a5 |
| 37 | planted_effect | 0.95 | 200 | 200 | e4f663f7ea364a68be838ee30e02809b |
| 38 | planted_effect | 0.95 | 200 | 200 | 78db8509b309c33126520f6597209f72 |
| 39 | planted_effect | 0.95 | 200 | 200 | ddaf0c193a1f1f351d13b8cfe1f1bb41 |
| 40 | planted_effect | 0.95 | 200 | 200 | 32754c8fa6bf689d73e1e704823f65a0 |
| 41 | planted_effect | 0.95 | 200 | 200 | aaf77666f5aded162d3840487b554fdd |
| 42 | planted_effect | 0.95 | 200 | 200 | 59bcef8fc57cebb3ecb0a7f8f5f54233 |
| 43 | planted_effect | 0.95 | 200 | 200 | f216988daa224a45f46163f7a5b2b322 |
| 44 | planted_effect | 0.95 | 200 | 200 | 858223eebef8cb45472954a6da9a0649 |
| 45 | planted_effect | 0.95 | 200 | 200 | 77ff322791f1f12d408fbd01a6496ee5 |
| 46 | planted_effect | 0.95 | 200 | 200 | ca0f77b5939381ebb4450fc367dc839a |
| 47 | planted_effect | 0.95 | 200 | 200 | e205fa06e582c81e68bb07582c3b42a4 |
| 48 | planted_effect | 0.98 | 200 | 200 | b3ed96a5173ba9ca6218aeaaf8be6a87 |
| 49 | planted_effect | 0.98 | 200 | 200 | b3bfb48321c67d27387a63d1c90f29c3 |
| 50 | planted_effect | 0.98 | 200 | 200 | f48de9e53a73120a2f2533cc88c404fa |
| 51 | planted_effect | 0.98 | 200 | 200 | f4e7157ed1a300b360b38db3d191ba51 |
| 52 | planted_effect | 0.98 | 200 | 200 | e15d784bc24109751ec3adf448e31f58 |
| 53 | planted_effect | 0.98 | 200 | 200 | 9450fab63ba0ffcade82d3ccb64b2fd7 |
| 54 | planted_effect | 0.98 | 200 | 200 | d3e5b368bc9fe608a5b691bf6a58fec8 |
| 55 | planted_effect | 0.98 | 200 | 200 | 7c16079a6fe61247ae7d732e17f66fdc |
| 56 | planted_effect | 0.98 | 200 | 200 | 4cc5e3b7fad020bc766e2bb54619b6d7 |
| 57 | planted_effect | 0.98 | 200 | 200 | 013e24bb3c39781576a190a89120b3c5 |
| 58 | planted_effect | 0.98 | 200 | 200 | 167702baea89bdb6595dd5b131bf5bb5 |
| 59 | planted_effect | 0.98 | 200 | 200 | 61aecfbce249798c77e6a44cae575764 |
| 60 | regime_span | 0.5 | 200 | 200 | 7cdca4067d3330422c68084e2dcc5419 |
| 61 | regime_span | 0.5 | 200 | 200 | ef86be2064973ea13a8894e42cd90cce |
| 62 | regime_span | 0.5 | 200 | 200 | 7da7808646a1287f31daf86b9f450da2 |
| 63 | regime_span | 0.5 | 200 | 200 | 2dd65d4f56575e0f7f4615432ce09ede |
| 64 | regime_span | 0.8 | 200 | 200 | d2ec03d83378cf80b69470561bafd7d9 |
| 65 | regime_span | 0.8 | 200 | 200 | 9f4c7776da633f0e8761546e146be9a0 |
| 66 | regime_span | 0.8 | 200 | 200 | ad3f31cc8331a2b72381ca6a39c639e5 |
| 67 | regime_span | 0.8 | 200 | 200 | b02ea1319271046ec1e7e1cedda80526 |
| 68 | regime_span | 0.9 | 200 | 200 | eac845a9f1c8f23a288e40ac95ace606 |
| 69 | regime_span | 0.9 | 200 | 200 | ce8d4c609acc61b98feba5d0bf12cefe |
| 70 | regime_span | 0.9 | 200 | 200 | bff82a71e29a4a8225357d3f955b3371 |
| 71 | regime_span | 0.9 | 200 | 200 | dcba9b5e17c4183b913f6bb771c06801 |
| 72 | regime_span | 0.95 | 200 | 200 | 45af92d4617bff21aeba2d9781c7e2d8 |
| 73 | regime_span | 0.95 | 200 | 200 | 48d62d27d1697a69a8e32e3d2b012eb7 |
| 74 | regime_span | 0.95 | 200 | 200 | 17f99c449d82596efcc207512dff32f9 |
| 75 | regime_span | 0.95 | 200 | 200 | 55ad56d10b516b929d645afef5c3b765 |
| 76 | regime_span | 0.98 | 200 | 200 | b98b5aac173e9aaac2796ea8767889f8 |
| 77 | regime_span | 0.98 | 200 | 200 | 36934fddcf0daebe9953c464a274b9ad |
| 78 | regime_span | 0.98 | 200 | 200 | a45bccd4a21a74df9b5f798d72e5e363 |
| 79 | regime_span | 0.98 | 200 | 200 | aa5f5d346d6cda5e30647543e06988a9 |
| 80 | planted_null | 0.5 | 200 | 200 | bf2c9c46ceb8e8ae48b37ef83b250ed8 |
| 81 | planted_null | 0.8 | 200 | 200 | 5e2b917e56263fc967a0fa144faa9f27 |
| 82 | planted_null | 0.9 | 200 | 200 | e873ab109a7e66d0a4cfdc5a74080180 |
| 83 | planted_null | 0.95 | 200 | 200 | c2279c7a9f849534e0131f2c29025627 |
| 84 | planted_null | 0.98 | 200 | 200 | c23cdde7a6c68649399b0542bdca738e |
| 85 | surge_null | 0.5 | 200 | 200 | 880778e26ebcc57f9e8ec517eeff68b7 |
| 86 | surge_effect | 0.5 | 200 | 200 | 313c46d962e0131560e4a266e31064c2 |
| 87 | surge_null | 0.8 | 200 | 200 | d613ad35f8b0a91c369ff3e464950ba9 |
| 88 | surge_effect | 0.8 | 200 | 200 | 532c3991d3fa6de11b82d7cdbe9353e1 |
| 89 | surge_null | 0.9 | 200 | 200 | 8f97be9b273a34613dfa8c868f278dde |
| 90 | surge_effect | 0.9 | 200 | 200 | 30cb2935e88ee0564ab0b1d3a30ecd46 |
| 91 | surge_null | 0.95 | 200 | 200 | 28f202472a50fd58354350e7f6fce71e |
| 92 | surge_effect | 0.95 | 200 | 200 | baa9859c67068fe227ffe16ac8bbc704 |
| 93 | surge_null | 0.98 | 200 | 200 | 1be5b4aa7e8297b5c7b1f4b62affd9f7 |
| 94 | surge_effect | 0.98 | 200 | 200 | ea27ae035eda2a96da3ffa67ac796bf8 |
| 95 | t3_null | 0.5 | 200 | 200 | e436fd29fde13d676eec8f5764c4de01 |
| 96 | t3_null | 0.8 | 200 | 200 | 2b1906af11edcbc4fc06e31bea4dc4c7 |
| 97 | t3_null | 0.9 | 200 | 200 | f00486b5346ba251588d3c1fc88c49fe |
| 98 | t3_null | 0.95 | 200 | 200 | 3c27e9586b28afe406e35f1e87e24275 |
| 99 | t3_null | 0.98 | 200 | 200 | 9c3f09e88ed9df54472da9b679d3a49d |
| 105 | decision_flip | 0.5 | 200 | 200 | 6d9ead1ec7bd49f693748bd73810eaa6 |
| 106 | t3_decision_flip | 0.5 | 200 | 200 | ca522662729c28130926ec27d00327f3 |
| 107 | decision_flip | 0.8 | 200 | 200 | 31e4278e7143e6ec33670d6b6dcd02e5 |
| 108 | t3_decision_flip | 0.8 | 200 | 200 | bda2ed28642a183f97b5f914da08ac5c |
| 109 | decision_flip | 0.9 | 200 | 200 | 6f7d7bcb573893d55ba7a24f337e349d |
| 110 | t3_decision_flip | 0.9 | 200 | 200 | aebf85e3c88232efcac9b07136a880ed |
| 111 | decision_flip | 0.95 | 200 | 200 | 26f8d8894e3cdf762aafec190c15bf6b |
| 112 | t3_decision_flip | 0.95 | 200 | 200 | 4a2c08b3f1f23814988a331131b57485 |
| 113 | decision_flip | 0.98 | 200 | 200 | 8087076a1e49ac70dbb0778fe5b61077 |
| 114 | t3_decision_flip | 0.98 | 200 | 200 | 5ab6dd37238bf1f2ec2a0273391b4b2c |
