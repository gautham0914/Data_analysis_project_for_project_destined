# Real Estate SQL Results

This report lists each analytical question and its output table.

## Top states by average home value

Source CSV: `01_top_avg_home_value.csv`


| state_name           |   avg_home_value |
|:---------------------|-----------------:|
| Hawaii               |           728940 |
| California           |           670742 |
| District of Columbia |           631433 |
| Washington           |           523857 |
| Massachusetts        |           518148 |
| Colorado             |           495760 |
| Utah                 |           461124 |
| Oregon               |           452137 |
| Idaho                |           406541 |
| New Jersey           |           405956 |
| New York             |           385918 |
| Nevada               |           379098 |
| New Hampshire        |           377896 |
| Rhode Island         |           372288 |
| Montana              |           368896 |

_Showing first 15 rows. Full output is in the CSV file._



---

## Top states by growth (first quarter to last quarter)

Source CSV: `02_growth_first_last.csv`


| state_name     |   growth_pct |
|:---------------|-------------:|
| Montana        |        57.43 |
| Florida        |        53.58 |
| Georgia        |        51.54 |
| North Carolina |        51.22 |
| Maine          |        51.02 |
| Idaho          |        49.68 |
| Tennessee      |        49.57 |
| Arizona        |        49.33 |
| South Carolina |        47.36 |
| Kansas         |        46.77 |
| New Hampshire  |        46.01 |
| Oklahoma       |        43.58 |
| Utah           |        43.05 |
| Vermont        |        43    |
| New Mexico     |        42.03 |

_Showing first 15 rows. Full output is in the CSV file._



---

## Most volatile states (std dev of home values)

Source CSV: `03_volatility.csv`


| state_name    |   volatility |
|:--------------|-------------:|
| Hawaii        |      95121.6 |
| California    |      80362.9 |
| Utah          |      68954.3 |
| Idaho         |      68500.9 |
| Washington    |      67717.7 |
| Montana       |      65783.6 |
| Arizona       |      61629.9 |
| Colorado      |      59257.2 |
| Florida       |      55099.2 |
| Oregon        |      53131.2 |
| New Hampshire |      52554.3 |
| Massachusetts |      51659.7 |
| Nevada        |      50214.4 |
| Maine         |      46802.4 |
| Georgia       |      43066.4 |

_Showing first 15 rows. Full output is in the CSV file._



---

## Quarter-over-quarter growth by state and quarter

Source CSV: `04_qoq_growth.csv`


| state_name   |   year |   quarter_num |   median_home_value |   qoq_growth_pct |
|:-------------|-------:|--------------:|--------------------:|-----------------:|
| Connecticut  |   2020 |             1 |              272744 |           nan    |
| Connecticut  |   2020 |             2 |              277199 |             1.63 |
| Connecticut  |   2020 |             3 |              279135 |             0.7  |
| Connecticut  |   2020 |             4 |              289964 |             3.88 |
| Connecticut  |   2021 |             1 |              304915 |             5.16 |
| Connecticut  |   2021 |             2 |              318978 |             4.61 |
| Connecticut  |   2021 |             3 |              326837 |             2.46 |
| Connecticut  |   2021 |             4 |              326692 |            -0.04 |
| Connecticut  |   2022 |             1 |              337525 |             3.32 |
| Connecticut  |   2022 |             2 |              355354 |             5.28 |
| Connecticut  |   2022 |             3 |              364017 |             2.44 |
| Connecticut  |   2022 |             4 |              363674 |            -0.09 |
| Connecticut  |   2023 |             1 |              366202 |             0.7  |
| Louisiana    |   2020 |             1 |              164544 |           nan    |
| Louisiana    |   2020 |             2 |              166875 |             1.42 |

_Showing first 15 rows. Full output is in the CSV file._



---

## Year-over-year growth by state and quarter

Source CSV: `05_yoy_growth.csv`


| state_name   |   year |   quarter_num |   median_home_value |   yoy_growth_pct |
|:-------------|-------:|--------------:|--------------------:|-----------------:|
| Arizona      |   2020 |             1 |              279275 |           nan    |
| Arizona      |   2020 |             2 |              287018 |           nan    |
| Arizona      |   2020 |             3 |              293132 |           nan    |
| Arizona      |   2020 |             4 |              306570 |           nan    |
| Arizona      |   2021 |             1 |              322957 |            15.64 |
| Arizona      |   2021 |             2 |              345398 |            20.34 |
| Arizona      |   2021 |             3 |              371179 |            26.63 |
| Arizona      |   2021 |             4 |              390817 |            27.48 |
| Arizona      |   2022 |             1 |              409885 |            26.92 |
| Arizona      |   2022 |             2 |              435798 |            26.17 |
| Arizona      |   2022 |             3 |              446272 |            20.23 |
| Arizona      |   2022 |             4 |              431170 |            10.33 |
| Arizona      |   2023 |             1 |              417042 |             1.75 |
| Kansas       |   2020 |             1 |              144480 |           nan    |
| Kansas       |   2020 |             2 |              146043 |           nan    |

_Showing first 15 rows. Full output is in the CSV file._



---

## High value + high growth (combined ranking)

Source CSV: `06_high_value_high_growth.csv`


| state_name           |   avg_value |   growth_pct |
|:---------------------|------------:|-------------:|
| Hawaii               |      728940 |        35.53 |
| California           |      670742 |        31.48 |
| District of Columbia |      631433 |         8.33 |
| Washington           |      523857 |        37.03 |
| Massachusetts        |      518148 |        29.83 |
| Colorado             |      495760 |        32.73 |
| Utah                 |      461124 |        43.05 |
| Oregon               |      452137 |        32.56 |
| Idaho                |      406541 |        49.68 |
| New Jersey           |      405956 |        33.01 |
| New York             |      385918 |        27.9  |
| Nevada               |      379098 |        33.06 |
| New Hampshire        |      377896 |        46.01 |
| Rhode Island         |      372288 |        35.85 |
| Montana              |      368896 |        57.43 |

_Showing first 15 rows. Full output is in the CSV file._



---

## Recent momentum (last 2 quarters growth)

Source CSV: `07_recent_momentum.csv`


| state_name     |   last_2q_growth_pct |
|:---------------|---------------------:|
| Kentucky       |                 1.76 |
| Oklahoma       |                 1.69 |
| Vermont        |                 1.66 |
| Kansas         |                 1.59 |
| Alabama        |                 1.55 |
| Arkansas       |                 1.54 |
| Wyoming        |                 1.16 |
| Wisconsin      |                 1.06 |
| Iowa           |                 0.83 |
| Nebraska       |                 0.81 |
| Ohio           |                 0.69 |
| North Dakota   |                 0.61 |
| Connecticut    |                 0.6  |
| Pennsylvania   |                 0.59 |
| South Carolina |                 0.57 |

_Showing first 15 rows. Full output is in the CSV file._



---
