# D.5 suite verdict — statistical cells

Graded from `scripts/outputs/suite_v1` by `scripts/suite/grade_suite.py`.

**FAIL (10: ['dr_grid10 0.5', 'dr_grid10 0.8', 'dr_grid10 0.9', 'dr_grid10 0.95', 'dr_grid10 0.98', 'dr_step 0.5', 'dr_step 0.8', 'dr_step 0.9', 'dr_step 0.95', 'dr_step 0.98'])**

| cell | kind | result | verdict |
|---|---|---|---|
| licence | analysis/ops.py | unchanged since aad6cf7 | PASS |
| licence | analysis/pipeline.py | unchanged since aad6cf7 | PASS |
| licence | analysis/e2stat.py | unchanged since aad6cf7 | PASS |
| licence | reference/ref_e2.py | unchanged since aad6cf7 | PASS |
| agreement | reference agreement (8.1) on 260 E2-chain cells | complete and all identical | PASS |
| 0 | planted_effect (phi=0.5, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.050/0.280/0.670 | mean lead B1 1.6, B2 2.1, B3 1.5, B4 3.3, D_div 3.5 | REPORTED |
| 1 | planted_effect (phi=0.5, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.075/0.325/0.600 | mean lead B1 2.0, B2 6.2, B3 2.6, B4 13.0, D_div 12.6 | REPORTED |
| 2 | planted_effect (phi=0.5, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.040/0.225/0.735 | mean lead B1 2.1, B2 15.9, B3 2.9, B4 25.3, D_div 20.3 | REPORTED |
| 3 | planted_effect (phi=0.5, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.045/0.345/0.610 | mean lead B1 2.2, B2 3.5, B3 2.1, B4 6.1, D_div 6.3 | REPORTED |
| 4 | planted_effect (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.100/0.410/0.490 | mean lead B1 2.1, B2 12.1, B3 3.3, B4 24.0, D_div 23.5 | REPORTED |
| 5 | planted_effect (phi=0.5, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.070/0.260/0.670 | mean lead B1 2.8, B2 29.3, B3 4.1, B4 44.1, D_div 37.3 | REPORTED |
| 6 | planted_effect (phi=0.5, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.440/0.540 | mean lead B1 1.7, B2 4.8, B3 1.9, B4 9.5, D_div 9.7 | REPORTED |
| 7 | planted_effect (phi=0.5, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.095/0.420/0.485 | mean lead B1 2.7, B2 24.9, B3 3.4, B4 37.4, D_div 37.7 | REPORTED |
| 8 | planted_effect (phi=0.5, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.125/0.240/0.635 | mean lead B1 3.6, B2 54.0, B3 5.9, B4 69.6, D_div 60.8 | REPORTED |
| 9 | planted_effect (phi=0.5, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.030/0.370/0.600 | mean lead B1 1.9, B2 8.0, B3 2.7, B4 10.8, D_div 10.7 | REPORTED |
| 10 | planted_effect (phi=0.5, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.060/0.315/0.625 | mean lead B1 2.3, B2 36.1, B3 4.1, B4 41.0, D_div 38.9 | REPORTED |
| 11 | planted_effect (phi=0.5, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.050/0.210/0.740 | mean lead B1 3.0, B2 73.2, B3 5.6, B4 79.3, D_div 66.8 | REPORTED |
| 12 | planted_effect (phi=0.8, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.210/0.775 | mean lead B1 1.6, B2 1.7, B3 1.7, B4 2.6, D_div 1.9 | REPORTED |
| 13 | planted_effect (phi=0.8, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.240/0.750 | mean lead B1 1.4, B2 5.3, B3 2.2, B4 5.9, D_div 4.9 | REPORTED |
| 14 | planted_effect (phi=0.8, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.195/0.795 | mean lead B1 1.7, B2 12.8, B3 2.6, B4 13.8, D_div 11.2 | REPORTED |
| 15 | planted_effect (phi=0.8, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.205/0.785 | mean lead B1 1.5, B2 3.2, B3 1.8, B4 4.1, D_div 3.2 | REPORTED |
| 16 | planted_effect (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.195/0.785 | mean lead B1 1.9, B2 10.4, B3 2.6, B4 11.9, D_div 9.4 | REPORTED |
| 17 | planted_effect (phi=0.8, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | mean lead B1 2.4, B2 25.2, B3 3.9, B4 26.7, D_div 21.2 | REPORTED |
| 18 | planted_effect (phi=0.8, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.155/0.830 | mean lead B1 2.0, B2 5.5, B3 2.6, B4 6.5, D_div 4.4 | REPORTED |
| 19 | planted_effect (phi=0.8, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | mean lead B1 2.4, B2 20.2, B3 3.6, B4 19.7, D_div 14.4 | REPORTED |
| 20 | planted_effect (phi=0.8, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.045/0.950 | mean lead B1 2.8, B2 44.7, B3 4.5, B4 44.3, D_div 32.3 | REPORTED |
| 21 | planted_effect (phi=0.8, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.9, B2 7.7, B3 3.2, B4 7.6, D_div 5.2 | REPORTED |
| 22 | planted_effect (phi=0.8, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 2.1, B2 31.7, B3 3.8, B4 24.0, D_div 14.7 | REPORTED |
| 23 | planted_effect (phi=0.8, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 2.9, B2 63.4, B3 5.3, B4 52.5, D_div 31.3 | REPORTED |
| 24 | planted_effect (phi=0.9, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.215/0.785 | mean lead B1 1.3, B2 1.8, B3 1.4, B4 1.8, D_div 1.6 | REPORTED |
| 25 | planted_effect (phi=0.9, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 1.5, B2 4.7, B3 2.0, B4 4.0, D_div 3.1 | REPORTED |
| 26 | planted_effect (phi=0.9, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | mean lead B1 1.8, B2 11.2, B3 3.1, B4 7.7, D_div 6.9 | REPORTED |
| 27 | planted_effect (phi=0.9, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.185/0.810 | mean lead B1 1.6, B2 2.9, B3 2.0, B4 3.1, D_div 2.2 | REPORTED |
| 28 | planted_effect (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | mean lead B1 2.0, B2 8.5, B3 2.8, B4 6.5, D_div 5.7 | REPORTED |
| 29 | planted_effect (phi=0.9, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | mean lead B1 2.1, B2 21.6, B3 4.2, B4 15.7, D_div 13.4 | REPORTED |
| 30 | planted_effect (phi=0.9, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | mean lead B1 2.0, B2 5.0, B3 2.3, B4 4.4, D_div 3.4 | REPORTED |
| 31 | planted_effect (phi=0.9, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 2.5, B2 17.6, B3 3.9, B4 12.6, D_div 8.8 | REPORTED |
| 32 | planted_effect (phi=0.9, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | mean lead B1 3.1, B2 39.6, B3 5.5, B4 28.1, D_div 19.4 | REPORTED |
| 33 | planted_effect (phi=0.9, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.120/0.880 | mean lead B1 1.8, B2 7.1, B3 2.5, B4 5.3, D_div 3.7 | REPORTED |
| 34 | planted_effect (phi=0.9, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.030/0.970 | mean lead B1 2.6, B2 25.0, B3 3.8, B4 15.9, D_div 7.8 | REPORTED |
| 35 | planted_effect (phi=0.9, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 2.4, B2 54.9, B3 5.1, B4 34.6, D_div 18.7 | REPORTED |
| 36 | planted_effect (phi=0.95, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | mean lead B1 1.6, B2 2.2, B3 1.7, B4 1.8, D_div 1.5 | REPORTED |
| 37 | planted_effect (phi=0.95, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | mean lead B1 1.7, B2 4.6, B3 2.8, B4 2.6, D_div 2.9 | REPORTED |
| 38 | planted_effect (phi=0.95, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | mean lead B1 1.6, B2 10.7, B3 3.1, B4 4.8, D_div 5.5 | REPORTED |
| 39 | planted_effect (phi=0.95, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.195/0.805 | mean lead B1 1.5, B2 3.1, B3 2.3, B4 2.4, D_div 2.2 | REPORTED |
| 40 | planted_effect (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | mean lead B1 1.7, B2 8.5, B3 2.4, B4 4.8, D_div 4.9 | REPORTED |
| 41 | planted_effect (phi=0.95, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 2.2, B2 19.1, B3 3.9, B4 9.4, D_div 9.2 | REPORTED |
| 42 | planted_effect (phi=0.95, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | mean lead B1 1.6, B2 4.5, B3 2.2, B4 3.4, D_div 2.9 | REPORTED |
| 43 | planted_effect (phi=0.95, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.060/0.935 | mean lead B1 1.8, B2 14.3, B3 2.8, B4 8.1, D_div 5.8 | REPORTED |
| 44 | planted_effect (phi=0.95, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | mean lead B1 2.3, B2 34.6, B3 5.5, B4 16.1, D_div 13.9 | REPORTED |
| 45 | planted_effect (phi=0.95, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | mean lead B1 1.6, B2 6.6, B3 2.0, B4 4.9, D_div 3.0 | REPORTED |
| 46 | planted_effect (phi=0.95, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | mean lead B1 2.6, B2 22.9, B3 4.3, B4 11.9, D_div 7.5 | REPORTED |
| 47 | planted_effect (phi=0.95, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 2.3, B2 47.3, B3 5.6, B4 22.0, D_div 12.4 | REPORTED |
| 48 | planted_effect (phi=0.98, n_events=20, L=64, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.170/0.820 | mean lead B1 1.3, B2 2.0, B3 1.4, B4 1.5, D_div 1.5 | REPORTED |
| 49 | planted_effect (phi=0.98, n_events=20, L=64, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.175/0.820 | mean lead B1 2.1, B2 4.2, B3 2.8, B4 2.3, D_div 2.9 | REPORTED |
| 50 | planted_effect (phi=0.98, n_events=20, L=64, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.110/0.885 | mean lead B1 1.8, B2 10.1, B3 3.8, B4 3.3, D_div 5.6 | REPORTED |
| 51 | planted_effect (phi=0.98, n_events=20, L=100, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.200/0.800 | mean lead B1 1.6, B2 2.9, B3 1.8, B4 2.1, D_div 2.4 | REPORTED |
| 52 | planted_effect (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.130/0.860 | mean lead B1 2.2, B2 7.2, B3 3.3, B4 3.5, D_div 4.0 | REPORTED |
| 53 | planted_effect (phi=0.98, n_events=20, L=100, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.070/0.925 | mean lead B1 2.4, B2 17.2, B3 4.2, B4 7.0, D_div 9.0 | REPORTED |
| 54 | planted_effect (phi=0.98, n_events=20, L=150, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | mean lead B1 1.7, B2 3.9, B3 2.4, B4 3.3, D_div 2.7 | REPORTED |
| 55 | planted_effect (phi=0.98, n_events=20, L=150, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.090/0.900 | mean lead B1 1.7, B2 12.9, B3 3.9, B4 5.5, D_div 5.9 | REPORTED |
| 56 | planted_effect (phi=0.98, n_events=20, L=150, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.050/0.945 | mean lead B1 2.4, B2 29.1, B3 5.8, B4 12.3, D_div 13.9 | REPORTED |
| 57 | planted_effect (phi=0.98, n_events=20, L=200, A=1.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.200/0.800 | mean lead B1 1.4, B2 5.5, B3 1.9, B4 4.2, D_div 3.6 | REPORTED |
| 58 | planted_effect (phi=0.98, n_events=20, L=200, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | mean lead B1 2.1, B2 18.3, B3 4.0, B4 8.5, D_div 6.9 | REPORTED |
| 59 | planted_effect (phi=0.98, n_events=20, L=200, A=3.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 2.1, B2 39.4, B3 5.3, B4 15.6, D_div 12.6 | REPORTED |
| 60 | regime_span (phi=0.5, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.110/0.400/0.490 | mean lead B1 2.5, B2 12.8, B3 3.2, B4 22.9, D_div 25.4 | REPORTED |
| 61 | regime_span (phi=0.5, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.120/0.455/0.425 | mean lead B1 2.4, B2 12.8, B3 3.3, B4 22.3, D_div 24.1 | REPORTED |
| 62 | regime_span (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.110/0.370/0.520 | mean lead B1 1.9, B2 12.9, B3 2.5, B4 23.6, D_div 23.2 | REPORTED |
| 63 | regime_span (phi=0.5, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.190/0.305/0.505 | mean lead B1 2.0, B2 11.7, B3 2.9, B4 22.8, D_div 22.0 | REPORTED |
| 64 | regime_span (phi=0.8, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.235/0.760 | mean lead B1 2.2, B2 9.6, B3 2.9, B4 11.5, D_div 9.3 | REPORTED |
| 65 | regime_span (phi=0.8, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.020/0.245/0.735 | mean lead B1 2.0, B2 10.1, B3 2.4, B4 12.0, D_div 10.0 | REPORTED |
| 66 | regime_span (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.165/0.830 | mean lead B1 1.9, B2 10.6, B3 2.9, B4 11.8, D_div 8.9 | REPORTED |
| 67 | regime_span (phi=0.8, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.220/0.775 | mean lead B1 1.5, B2 9.1, B3 2.4, B4 11.4, D_div 8.5 | REPORTED |
| 68 | regime_span (phi=0.9, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 1.7, B2 9.5, B3 3.2, B4 7.5, D_div 6.0 | REPORTED |
| 69 | regime_span (phi=0.9, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | mean lead B1 1.6, B2 8.4, B3 2.3, B4 6.2, D_div 5.4 | REPORTED |
| 70 | regime_span (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | mean lead B1 1.5, B2 8.9, B3 2.8, B4 7.2, D_div 5.8 | REPORTED |
| 71 | regime_span (phi=0.9, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.140/0.850 | mean lead B1 1.6, B2 8.5, B3 2.5, B4 6.8, D_div 5.3 | REPORTED |
| 72 | regime_span (phi=0.95, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | mean lead B1 1.6, B2 8.2, B3 2.3, B4 4.4, D_div 4.4 | REPORTED |
| 73 | regime_span (phi=0.95, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.195/0.805 | mean lead B1 1.5, B2 7.7, B3 2.3, B4 4.2, D_div 4.5 | REPORTED |
| 74 | regime_span (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | mean lead B1 1.9, B2 7.9, B3 3.0, B4 4.6, D_div 4.4 | REPORTED |
| 75 | regime_span (phi=0.95, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | mean lead B1 1.5, B2 7.6, B3 2.4, B4 4.3, D_div 4.3 | REPORTED |
| 76 | regime_span (phi=0.98, n_events=5, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.185/0.815 | mean lead B1 1.9, B2 7.6, B3 1.7, B4 4.0, D_div 4.5 | REPORTED |
| 77 | regime_span (phi=0.98, n_events=10, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.160/0.840 | mean lead B1 2.7, B2 7.5, B3 3.1, B4 4.0, D_div 4.3 | REPORTED |
| 78 | regime_span (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.015/0.170/0.815 | mean lead B1 1.8, B2 7.9, B3 3.3, B4 4.1, D_div 5.1 | REPORTED |
| 79 | regime_span (phi=0.98, n_events=40, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.175/0.820 | mean lead B1 1.6, B2 7.0, B3 2.8, B4 3.8, D_div 4.3 | REPORTED |
| 80 | planted_null (phi=0.5, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | PASS |
| 81 | planted_null (phi=0.8, n_events=20) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 82 | planted_null (phi=0.9, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 83 | planted_null (phi=0.95, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 84 | planted_null (phi=0.98, n_events=20) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 85 | surge_null (phi=0.5, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 86 | surge_effect (phi=0.5, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.045/0.950 | mean lead B1 2.5, B2 8.7, B3 3.1, B4 0.6, D_div 2.8 | REPORTED |
| 87 | surge_null (phi=0.8, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 88 | surge_effect (phi=0.8, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.165/0.825 | mean lead B1 1.9, B2 8.5, B3 2.8, B4 2.2, D_div 4.2 | REPORTED |
| 89 | surge_null (phi=0.9, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | PASS |
| 90 | surge_effect (phi=0.9, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.115/0.885 | mean lead B1 2.0, B2 8.2, B3 2.7, B4 2.9, D_div 3.4 | REPORTED |
| 91 | surge_null (phi=0.95, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 92 | surge_effect (phi=0.95, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.120/0.880 | mean lead B1 1.5, B2 6.9, B3 2.7, B4 2.9, D_div 3.4 | REPORTED |
| 93 | surge_null (phi=0.98, n_events=20) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | PASS |
| 94 | surge_effect (phi=0.98, n_events=20, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | mean lead B1 2.3, B2 6.8, B3 2.9, B4 2.7, D_div 3.4 | REPORTED |
| 95 | t3_null (phi=0.5, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.150/0.850 | PASS |
| 96 | t3_null (phi=0.8, n_events=20, innov=t3) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 97 | t3_null (phi=0.9, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 98 | t3_null (phi=0.95, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | PASS |
| 99 | t3_null (phi=0.98, n_events=20, innov=t3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.125/0.875 | PASS |
| 115 | unequal_memory_null (phi=0.5, n_events=20) | false-SUPPORT 0.005 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.775, P(C_b>0|C_b!=0) S1 0.511 S40 0.511; SUPPORT/INCONCL/REFUTE 0.005/0.220/0.775 | PASS |
| 116 | unequal_memory_null (phi=0.8, n_events=20) | false-SUPPORT 0.005 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 0.990 (>= 0.95); reported: false-REFUTE 0.795, P(C_b>0|C_b!=0) S1 0.471 S40 0.471; SUPPORT/INCONCL/REFUTE 0.005/0.200/0.795 | PASS |
| 117 | unequal_memory_null (phi=0.9, n_events=20) | false-SUPPORT 0.010 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.790, P(C_b>0|C_b!=0) S1 0.467 S40 0.467; SUPPORT/INCONCL/REFUTE 0.010/0.200/0.790 | PASS |
| 118 | unequal_memory_null (phi=0.95, n_events=20) | false-SUPPORT 0.010 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 1.000 (>= 0.95); reported: false-REFUTE 0.770, P(C_b>0|C_b!=0) S1 0.517 S40 0.517; SUPPORT/INCONCL/REFUTE 0.010/0.220/0.770 | PASS |
| 119 | unequal_memory_null (phi=0.98, n_events=20) | false-SUPPORT 0.000 (<= 0.05); max|median C_b| 0.00 (<= 1); share |C_S1-C_S40|<=1 0.965 (>= 0.95); reported: false-REFUTE 0.760, P(C_b>0|C_b!=0) S1 0.551 S40 0.511; SUPPORT/INCONCL/REFUTE 0.000/0.240/0.760 | PASS |
| 120 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 121 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 122 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 123 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 124 | null_pulse_sweep (phi=0.5, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 125 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 126 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 127 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 128 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | PASS |
| 129 | null_pulse_sweep (phi=0.8, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 130 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 131 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 132 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 133 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 134 | null_pulse_sweep (phi=0.9, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 135 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 136 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 137 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 138 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 139 | null_pulse_sweep (phi=0.95, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 140 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=D_div) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 141 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B1) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 142 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B2) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 143 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B3) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 144 | null_pulse_sweep (phi=0.98, n_events=20, pulse_for=B4) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | PASS |
| 145 | step_characterization (phi=0.5, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.025/0.240/0.735 | mean lead B1 3.1, B2 22.6, B3 4.4, B4 42.6, D_div 37.1 | REPORTED |
| 146 | step_characterization (phi=0.5, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.030/0.970 | mean lead B1 5.7, B2 42.6, B3 9.5, B4 54.1, D_div 43.4 | REPORTED |
| 147 | step_characterization (phi=0.5, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 10.8, B2 53.4, B3 15.8, B4 57.8, D_div 45.4 | REPORTED |
| 148 | step_characterization (phi=0.8, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.255/0.740 | mean lead B1 3.2, B2 19.1, B3 5.6, B4 20.9, D_div 17.8 | REPORTED |
| 149 | step_characterization (phi=0.8, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.005/0.135/0.860 | mean lead B1 5.9, B2 35.2, B3 11.1, B4 36.4, D_div 31.3 | REPORTED |
| 150 | step_characterization (phi=0.8, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 11.8, B2 48.7, B3 20.8, B4 47.3, D_div 40.0 | REPORTED |
| 151 | step_characterization (phi=0.9, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.145/0.855 | mean lead B1 4.1, B2 15.9, B3 7.8, B4 12.0, D_div 10.7 | REPORTED |
| 152 | step_characterization (phi=0.9, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | mean lead B1 8.7, B2 29.4, B3 15.7, B4 22.1, D_div 19.2 | REPORTED |
| 153 | step_characterization (phi=0.9, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | mean lead B1 16.4, B2 44.6, B3 28.7, B4 33.9, D_div 31.1 | REPORTED |
| 154 | step_characterization (phi=0.95, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 7.7, B2 14.4, B3 13.9, B4 8.2, D_div 7.9 | REPORTED |
| 155 | step_characterization (phi=0.95, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | mean lead B1 15.6, B2 25.1, B3 25.6, B4 13.5, D_div 14.3 | REPORTED |
| 156 | step_characterization (phi=0.95, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 26.5, B2 39.1, B3 39.1, B4 20.8, D_div 21.6 | REPORTED |
| 157 | step_characterization (phi=0.98, n_events=20, step_h=1.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 20.4, B2 12.9, B3 28.7, B4 5.8, D_div 9.0 | REPORTED |
| 158 | step_characterization (phi=0.98, n_events=20, step_h=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 33.3, B2 22.7, B3 42.3, B4 10.5, D_div 15.0 | REPORTED |
| 159 | step_characterization (phi=0.98, n_events=20, step_h=2.5) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 45.5, B2 37.1, B3 53.9, B4 15.4, D_div 24.1 | REPORTED |
| 160 | realised_count_null (phi=0.5, n_events=57) | false-SUPPORT 0.005 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.005/0.145/0.850 | PASS |
| 162 | realised_count_effect (phi=0.5, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.150/0.300/0.550 | mean lead B1 2.1, B2 11.7, B3 3.2, B4 24.1, D_div 22.2 | REPORTED |
| 163 | realised_count_null (phi=0.8, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.205/0.795 | PASS |
| 165 | realised_count_effect (phi=0.8, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.205/0.785 | mean lead B1 1.9, B2 9.7, B3 2.9, B4 12.5, D_div 9.3 | REPORTED |
| 166 | realised_count_null (phi=0.9, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.170/0.830 | PASS |
| 168 | realised_count_effect (phi=0.9, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 1.7, B2 8.7, B3 3.1, B4 7.8, D_div 5.7 | REPORTED |
| 169 | realised_count_null (phi=0.95, n_events=57) | false-SUPPORT 0.010 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.010/0.160/0.830 | PASS |
| 171 | realised_count_effect (phi=0.95, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.080/0.910 | mean lead B1 1.9, B2 7.5, B3 2.9, B4 4.8, D_div 4.2 | REPORTED |
| 172 | realised_count_null (phi=0.98, n_events=57) | false-SUPPORT 0.000 (<= 0.05); SUPPORT/INCONCL/REFUTE 0.000/0.210/0.790 | PASS |
| 174 | realised_count_effect (phi=0.98, n_events=57, L=100, A=2.0) | reported; SUPPORT/INCONCL/REFUTE 0.010/0.145/0.845 | mean lead B1 1.6, B2 7.2, B3 3.3, B4 4.1, D_div 4.8 | REPORTED |
| 175 | decision_flip (phi=0.5, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | PASS |
| 176 | t3_decision_flip (phi=0.5, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.825 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.175/0.825 | PASS |
| 177 | decision_flip (phi=0.8, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.870 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 178 | t3_decision_flip (phi=0.8, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.845 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | PASS |
| 179 | decision_flip (phi=0.9, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.890 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | PASS |
| 180 | t3_decision_flip (phi=0.9, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.875 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | PASS |
| 181 | decision_flip (phi=0.95, n_events=20, L=8, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.905 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.090/0.905 | PASS |
| 182 | t3_decision_flip (phi=0.95, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 183 | decision_flip (phi=0.98, n_events=20, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.835 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.165/0.835 | PASS |
| 184 | t3_decision_flip (phi=0.98, n_events=20, L=8, A=3.0, innov=t3) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.890 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.110/0.890 | PASS |
| 185 | realised_count_flip (phi=0.5, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.845 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.155/0.845 | PASS |
| 186 | realised_count_flip (phi=0.8, n_events=57, L=8, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.865 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.005/0.130/0.865 | PASS |
| 187 | realised_count_flip (phi=0.9, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.860 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 188 | realised_count_flip (phi=0.95, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.860 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 189 | realised_count_flip (phi=0.98, n_events=57, L=8, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.950 (kill-rule power vs short precursor); SUPPORT/INCONCL/REFUTE 0.000/0.050/0.950 | PASS |
| 190 | flip_long (phi=0.5, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 2.7, B2 6.6, B3 3.4, B4 6.9, D_div 0.9 | REPORTED |
| 191 | flip_long (phi=0.5, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 2.3, B2 7.3, B3 3.0, B4 9.2, D_div 2.2 | REPORTED |
| 192 | flip_long (phi=0.8, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | mean lead B1 2.0, B2 6.1, B3 2.9, B4 3.2, D_div 1.3 | REPORTED |
| 193 | flip_long (phi=0.8, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 2.3, B2 9.1, B3 3.8, B4 6.4, D_div 2.3 | REPORTED |
| 194 | flip_long (phi=0.9, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 1.8, B2 6.0, B3 3.6, B4 1.9, D_div 1.2 | REPORTED |
| 195 | flip_long (phi=0.9, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | mean lead B1 1.8, B2 8.8, B3 3.8, B4 2.9, D_div 2.3 | REPORTED |
| 196 | flip_long (phi=0.95, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | mean lead B1 2.1, B2 6.2, B3 5.0, B4 1.5, D_div 1.5 | REPORTED |
| 197 | flip_long (phi=0.95, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | mean lead B1 2.2, B2 9.4, B3 5.1, B4 2.0, D_div 1.8 | REPORTED |
| 198 | flip_long (phi=0.98, n_events=20, L=16, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.020/0.980 | mean lead B1 3.6, B2 6.7, B3 8.7, B4 1.5, D_div 1.2 | REPORTED |
| 199 | flip_long (phi=0.98, n_events=20, L=24, A=from scripts/outputs/calibration_flip.json [phi][L]) | reported; SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | mean lead B1 3.1, B2 9.5, B3 9.3, B4 1.8, D_div 1.9 | REPORTED |
| 200 | grid10_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 201 | grid10_effect (phi=0.5, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.030/0.080/0.890 | mean lead B1 21.1, B2 60.9, B3 26.0, B4 138.3, D_div 74.0 | REPORTED |
| 202 | grid10_effect (phi=0.5, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.035/0.090/0.875 | mean lead B1 23.1, B2 125.8, B3 35.6, B4 244.6, D_div 157.9 | REPORTED |
| 203 | grid10_effect (phi=0.5, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.070/0.175/0.755 | mean lead B1 28.7, B2 243.0, B3 51.2, B4 394.6, D_div 307.5 | REPORTED |
| 204 | grid10_effect (phi=0.5, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.020/0.060/0.920 | mean lead B1 27.5, B2 335.0, B3 49.0, B4 376.7, D_div 230.0 | REPORTED |
| 206 | grid10_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | PASS |
| 207 | grid10_effect (phi=0.8, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.100/0.900 | mean lead B1 21.7, B2 55.9, B3 26.7, B4 65.3, D_div 39.1 | REPORTED |
| 208 | grid10_effect (phi=0.8, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.015/0.080/0.905 | mean lead B1 22.3, B2 105.0, B3 34.2, B4 136.2, D_div 82.3 | REPORTED |
| 209 | grid10_effect (phi=0.8, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 24.1, B2 201.2, B3 43.4, B4 227.6, D_div 133.6 | REPORTED |
| 210 | grid10_effect (phi=0.8, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 23.3, B2 274.8, B3 44.0, B4 251.2, D_div 97.6 | REPORTED |
| 212 | grid10_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 213 | grid10_effect (phi=0.9, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.125/0.865 | mean lead B1 17.8, B2 48.2, B3 26.9, B4 41.0, D_div 26.3 | REPORTED |
| 214 | grid10_effect (phi=0.9, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.095/0.905 | mean lead B1 19.4, B2 91.9, B3 33.3, B4 82.6, D_div 48.1 | REPORTED |
| 215 | grid10_effect (phi=0.9, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.030/0.965 | mean lead B1 24.6, B2 176.3, B3 45.1, B4 147.3, D_div 73.3 | REPORTED |
| 216 | grid10_effect (phi=0.9, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | mean lead B1 24.1, B2 237.7, B3 46.4, B4 179.1, D_div 58.8 | REPORTED |
| 218 | grid10_null (phi=0.95) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 219 | grid10_effect (phi=0.95, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.100/0.900 | mean lead B1 18.4, B2 45.1, B3 26.5, B4 31.5, D_div 17.8 | REPORTED |
| 220 | grid10_effect (phi=0.95, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.080/0.920 | mean lead B1 22.2, B2 84.8, B3 34.7, B4 55.3, D_div 30.9 | REPORTED |
| 221 | grid10_effect (phi=0.95, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | mean lead B1 20.6, B2 150.1, B3 42.9, B4 106.7, D_div 52.5 | REPORTED |
| 222 | grid10_effect (phi=0.95, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | mean lead B1 23.2, B2 202.3, B3 46.3, B4 132.1, D_div 40.8 | REPORTED |
| 224 | grid10_null (phi=0.98) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.075/0.925 | PASS |
| 225 | grid10_effect (phi=0.98, L=640, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.145/0.855 | mean lead B1 19.6, B2 43.6, B3 31.6, B4 24.0, D_div 23.2 | REPORTED |
| 226 | grid10_effect (phi=0.98, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.125/0.875 | mean lead B1 20.3, B2 76.2, B3 36.1, B4 48.9, D_div 35.7 | REPORTED |
| 227 | grid10_effect (phi=0.98, L=1500, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.085/0.915 | mean lead B1 22.4, B2 127.8, B3 46.1, B4 80.2, D_div 48.6 | REPORTED |
| 228 | grid10_effect (phi=0.98, L=2000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.025/0.975 | mean lead B1 22.5, B2 170.0, B3 49.2, B4 94.8, D_div 37.9 | REPORTED |
| 230 | e2e_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.180/0.820 | PASS |
| 231 | e2e_effect (phi=0.5, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.125/0.375/0.500 | mean lead B1 2.2, B2 12.7, B3 3.1, B4 23.9, D_div 23.7 | REPORTED |
| 232 | e2e_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.115/0.885 | PASS |
| 233 | e2e_effect (phi=0.8, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.025/0.185/0.790 | mean lead B1 1.7, B2 10.5, B3 2.3, B4 11.8, D_div 9.2 | REPORTED |
| 234 | e2e_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.135/0.865 | PASS |
| 235 | e2e_effect (phi=0.9, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.9, B2 9.2, B3 2.9, B4 7.3, D_div 6.2 | REPORTED |
| 236 | e2e_null (phi=0.95) | false-SUPPORT 0.005 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.155/0.840 | PASS |
| 237 | e2e_effect (phi=0.95, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.150/0.845 | mean lead B1 1.8, B2 8.2, B3 2.9, B4 4.8, D_div 4.8 | REPORTED |
| 238 | e2e_null (phi=0.98) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.000/0.140/0.860 | PASS |
| 239 | e2e_effect (phi=0.98, L=100, A=2.0) | reported; events recovered exactly in 200/200; SUPPORT/INCONCL/REFUTE 0.005/0.185/0.810 | mean lead B1 1.9, B2 7.3, B3 2.9, B4 3.9, D_div 4.7 | REPORTED |
| 240 | grid10_short (phi=0.5, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.965 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.035/0.965 | PASS |
| 241 | grid10_short (phi=0.8, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.955 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | PASS |
| 242 | grid10_short (phi=0.9, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.960 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | PASS |
| 243 | grid10_short (phi=0.95, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.940 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.060/0.940 | PASS |
| 244 | grid10_short (phi=0.98, L=200, A=2.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.985 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | PASS |
| 245 | a1s_null (phi=0.5) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 246 | a1s_flip (phi=0.5, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.920 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.075/0.920 | PASS |
| 247 | a1s_effect (phi=0.5, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.255/0.315/0.430 | mean lead B1 24.1, B2 121.3, B3 34.6, B4 242.5, D_div 250.6 | REPORTED |
| 248 | a1s_null (phi=0.8) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 249 | a1s_flip (phi=0.8, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.900 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.095/0.900 | PASS |
| 250 | a1s_effect (phi=0.8, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.015/0.175/0.810 | mean lead B1 23.3, B2 106.8, B3 33.3, B4 126.9, D_div 101.3 | REPORTED |
| 251 | a1s_null (phi=0.9) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.130/0.870 | PASS |
| 252 | a1s_flip (phi=0.9, L=80, A=3.0) | SUPPORT 0.005 (<= 0.05); reported: REFUTE 0.875 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.005/0.120/0.875 | PASS |
| 253 | a1s_effect (phi=0.9, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.155/0.845 | mean lead B1 19.0, B2 87.6, B3 30.8, B4 73.5, D_div 58.8 | REPORTED |
| 254 | a1s_null (phi=0.95) | false-SUPPORT 0.000 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.090/0.910 | PASS |
| 255 | a1s_flip (phi=0.95, L=80, A=3.0) | SUPPORT 0.010 (<= 0.05); reported: REFUTE 0.930 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.060/0.930 | PASS |
| 256 | a1s_effect (phi=0.95, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.105/0.895 | mean lead B1 19.0, B2 90.2, B3 31.9, B4 52.4, D_div 50.8 | REPORTED |
| 257 | a1s_null (phi=0.98) | false-SUPPORT 0.010 (<= 0.05); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.010/0.100/0.890 | PASS |
| 258 | a1s_flip (phi=0.98, L=80, A=3.0) | SUPPORT 0.000 (<= 0.05); reported: REFUTE 0.935 (kill-rule power vs short precursor); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.065/0.935 | PASS |
| 259 | a1s_effect (phi=0.98, L=1000, A=2.0) | reported; events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.225/0.775 | mean lead B1 22.5, B2 74.7, B3 34.3, B4 42.4, D_div 50.6 | REPORTED |
| 260 | dr_step (phi=0.5, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.040/0.960 | REPORTED |
| 261 | dr_step (phi=0.5, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.055/0.945 | REPORTED |
| 262 | dr_step (phi=0.5, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.045/0.955 | REPORTED |
| 263 | dr_grid10 (phi=0.5, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 264 | dr_grid10 (phi=0.5, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 265 | dr_grid10 (phi=0.5, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 266 | dr_step (phi=0.8, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | REPORTED |
| 267 | dr_step (phi=0.8, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.095/0.905 | REPORTED |
| 268 | dr_step (phi=0.8, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.005/0.055/0.940 | REPORTED |
| 269 | dr_grid10 (phi=0.8, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 270 | dr_grid10 (phi=0.8, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 271 | dr_grid10 (phi=0.8, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 272 | dr_step (phi=0.9, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | REPORTED |
| 273 | dr_step (phi=0.9, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 274 | dr_step (phi=0.9, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.005/0.995 | REPORTED |
| 275 | dr_grid10 (phi=0.9, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 276 | dr_grid10 (phi=0.9, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 277 | dr_grid10 (phi=0.9, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 278 | dr_step (phi=0.95, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 279 | dr_step (phi=0.95, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 280 | dr_step (phi=0.95, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 281 | dr_grid10 (phi=0.95, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 282 | dr_grid10 (phi=0.95, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 283 | dr_grid10 (phi=0.95, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 284 | dr_step (phi=0.98, n_events=20, L=25, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 285 | dr_step (phi=0.98, n_events=20, L=75, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.010/0.990 | REPORTED |
| 286 | dr_step (phi=0.98, n_events=20, L=125, A=6.0) | reported (graded as a group, Amendment 14.3); SUPPORT/INCONCL/REFUTE 0.000/0.015/0.985 | REPORTED |
| 287 | dr_grid10 (phi=0.98, L=250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 288 | dr_grid10 (phi=0.98, L=750, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| 289 | dr_grid10 (phi=0.98, L=1250, A=6.0) | reported (graded as a group, Amendment 14.3); events recovered exactly in 200/200; all ten residues of t_e mod 10 in every replicate; SUPPORT/INCONCL/REFUTE 0.000/0.000/1.000 | REPORTED |
| dyn-range | dr_grid10 phi=0.5 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [64,293] vs [148,506] OVERLAP, B2 [402,455] vs [719,805] sep, B4 [475,523] vs [841,892] sep | FAIL |
| dyn-range | dr_grid10 phi=0.8 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [107,321] vs [183,566] OVERLAP, B2 [364,431] vs [678,759] sep, B4 [368,434] vs [696,779] sep | FAIL |
| dyn-range | dr_grid10 phi=0.9 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [118,296] vs [233,532] OVERLAP, B2 [352,411] vs [638,730] sep, B4 [263,358] vs [558,680] sep | FAIL |
| dyn-range | dr_grid10 phi=0.95 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']) | FAIL |
| dyn-range | dr_grid10 phi=0.98 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']) | FAIL |
| dyn-range | dr_step phi=0.5 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [15,48] vs [26,82] OVERLAP, B2 [40,46] vs [72,82] sep, B4 [47,52] vs [83,90] sep | FAIL |
| dyn-range | dr_step phi=0.8 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2', 'B4']); (75,125): D_div [20,41] vs [35,72] OVERLAP, B2 [37,44] vs [66,77] sep, B4 [36,43] vs [67,78] sep | FAIL |
| dyn-range | dr_step phi=0.9 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [21,35] vs [32,62] OVERLAP, B2 [34,43] vs [63,75] sep, B4 [25,35] vs [51,67] sep | FAIL |
| dyn-range | dr_step phi=0.95 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [18,32] vs [31,54] OVERLAP, B2 [33,42] vs [59,72] sep, B4 [14,26] vs [35,53] sep | FAIL |
| dyn-range | dr_step phi=0.98 (L obs [25, 75, 125]) | (25,75): VACUOUS - D_div and >= 1 baseline must detect >= 80% at both L (eligible: ['B2']); (75,125): D_div [19,32] vs [32,56] OVERLAP, B2 [33,42] vs [58,71] sep | FAIL |
