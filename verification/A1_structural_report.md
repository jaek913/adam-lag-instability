# A1 structural report (DESIGN Amendment 1 A1.12; Amendment 2)

Generated 2026-10-31T15:12:21+00:00 by scripts/a1_structural_report.py. Step index, non-null masks and run metadata only; no metric value was read.

## Kept series (Amendment 2)

| block | steps | owners | grid obs | dropped | longest dropped run | earliest eligible t_e^g | eligible-anchor span (steps) | > 11,280 steps |
|---|---|---|---|---|---|---|---|---|
| 1–14,200 | 14,200 | run-001 | 1,420 | 0 | 0 | 11,290 | 2,920 | yes |
| 52,301–160,500 | 108,200 | run-008; run-010 | 10,820 | 0 | 0 | 63,590 | 96,920 | yes |
| 160,601–504,500 | 343,900 | run-013; run-016; run-017; run-018 | 34,390 | 0 | 0 | 171,890 | 332,620 | yes |

## Gaps

| range | steps | grid steps | detector-series gap | cause | restarts within |
|---|---|---|---|---|---|
| 14,201–52,300 | 38,100 | 3,810 | yes | owner run-002 unused; owner run-003 unused; owner run-004 unused; owner run-005 unused; owner run-006 unused; owner run-007 unused | run-002@14200, run-003@14500, run-004@39350, run-005@41400, run-006@42200, run-007@51450 |
| 160,501–160,600 | 100 | 10 | yes | owner run-011 unused | run-011@160500 |
| 504,501–543,360 | 38,860 | 3,886 | yes | owner run-019 unused; owner run-020 unused; owner run-021 unused; owner run-022 unused; owner run-023 unused; owner run-024 unused; owner run-025 unused | run-019@504500, run-020@505550, run-021@507000, run-022@508500, run-023@509200, run-024@511350, run-025@521000 |

## Detector series and false-alarm budget

- N (grid observations in the kept series): **46,630**
- Dropped grid observations: 0; longest consecutive run: 0
- Kept steps without a loss value: 0
- n* upper bounds before any exclusion (round-half-up of FA × N / 10,000): FA 0.5: 2, FA 1: 5, FA 2: 9, FA 5: 23

## Rewind portions of used segments (scored on their own series)

| segment | range | steps | grid steps |
|---|---|---|---|
| run-001 | 14,201–14,210 | 10 | 1 |
| run-008 | 73,101–73,110 | 10 | 1 |
| run-010 | 160,501–160,851 | 351 | 35 |
| run-013 | 212,001–212,965 | 965 | 96 |
| run-016 | 337,001–337,339 | 339 | 33 |
| run-018 | 504,501–504,510 | 10 | 1 |

## Superseded portions of unused segments (unscorable; lower bounds from served rows)

| segment | range | steps |
|---|---|---|
| run-002 | 14,501–14,900 | 400 |
| run-003 | 39,351–39,360 | 10 |
| run-004 | 41,401–41,410 | 10 |
| run-005 | 42,201–42,210 | 10 |
| run-006 | 51,451–51,460 | 10 |
| run-007 | 52,301–52,310 | 10 |
| run-009 | 73,101–73,378 | 278 |
| run-012 | 160,601–160,855 | 255 |
| run-019 | 505,551–505,560 | 10 |
| run-020 | 507,001–507,010 | 10 |
| run-021 | 508,501–508,510 | 10 |
| run-022 | 509,201–509,210 | 10 |
| run-023 | 511,351–511,360 | 10 |
| run-024 | 521,001–521,010 | 10 |

## Segments

| segment | id | resume step | used | server lines | logged span | basis |
|---|---|---|---|---|---|---|
| run-001 | ucv77bvt | — | yes | 14,211 | 1–14,210 | measured loss span (route-1 file) |
| run-002 | yvnxfxho | 14,200 | no | 701 | 14,201–14,900 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-003 | s9gkykls | 14,500 | no | 24,861 | 14,501–39,360 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-004 | auqmzpj6 | 39,350 | no | 2,061 | 39,351–41,410 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-005 | gvf17mtk | 41,400 | no | 811 | 41,401–42,210 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-006 | ahhqn92q | 42,200 | no | 9,261 | 42,201–51,460 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-007 | wx1kidf5 | 51,450 | no | 861 | 51,451–52,310 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-008 | bnzb4pmk | 52,300 | yes | 20,811 | 52,301–73,110 | measured loss span (route-1 file) |
| run-009 | 7wdi29fz | 73,100 | no | 279 | 73,101–73,378 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-010 | wqjq7xzw | 73,100 | yes | 87,752 | 73,101–160,851 | measured loss span (route-1 file) |
| run-011 | 2j6q2kz8 | 160,500 | no | 100 | 160,501–160,599 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-012 | 56ru0hsd | 160,600 | no | 256 | 160,601–160,855 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-013 | 7lr31kjd | 160,600 | yes | 52,366 | 160,601–212,965 | measured loss span (route-1 file) |
| run-014 | vtnbhkmu | 212,000 | no | 1 | — | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-015 | bxzbwm3j | 212,000 | no | 1 | — | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-016 | 0g0rjkxo | 212,000 | yes | 125,340 | 212,001–337,339 | measured loss span (route-1 file) |
| run-017 | d4g44zcc | 337,000 | yes | 71,924 | 337,001–408,923 | measured loss span (route-1 file) |
| run-018 | 50br7dzw | 408,923 | yes | 95,587 | 408,924–504,510 | measured loss span (route-1 file) |
| run-019 | m22a5wug | 504,500 | no | 1,061 | 504,501–505,560 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-020 | iryle1e4 | 505,550 | no | 1,461 | 505,551–507,010 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-021 | eidrl8dn | 507,000 | no | 1,511 | 507,001–508,510 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-022 | x1jigg0a | 508,500 | no | 711 | 508,501–509,210 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-023 | l3qs9hoe | 509,200 | no | 2,161 | 509,201–511,360 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-024 | gqph7y8y | 511,350 | no | 9,661 | 511,351–521,010 | resume+1 .. served last row (lower bound; Addendum B item 8) |
| run-025 | u3obk6mj | 521,000 | no | 22,361 | 521,001–543,360 | resume+1 .. served last row (lower bound; Addendum B item 8) |
