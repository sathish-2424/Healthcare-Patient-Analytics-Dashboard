# Healthcare Patient Analytics Dashboard

This repository contains a healthcare analytics dataset and two dashboard builds used to explore patient, billing, and operational trends.

The project is centered on a patient-level dataset with 55,501 records and includes both Power BI and Tableau dashboard files for analysis and visualization.

## What Is Included

- `healthcare.csv` - source dataset
- `Healthcare Patient Analytics Dashboard.pbix` - Power BI report
- `Healthcare Patient Analytics Dashboard.twb` - Tableau workbook
- `dashboard.png` - dashboard preview image
- `dashboard2.png` - additional dashboard preview image

## Dataset Overview

The dataset includes the following fields:

- Patient name
- Age
- Gender
- Blood type
- Medical condition
- Date of admission
- Doctor
- Hospital
- Insurance provider
- Billing amount
- Room number
- Admission type
- Discharge date
- Medication
- Test results

## Dashboard Focus

The dashboards are designed to analyze:

- Revenue and billing patterns
- Patient volume
- Average length of stay
- Admission type distribution
- Hospital-level performance
- Doctor-level billing activity
- Medical condition trends
- Demographic breakdowns by age and gender

## Example KPIs

The report surfaces summary metrics such as:

- Total revenue
- Total patients
- Average billing amount
- Average length of stay

## How To Use

1. Open `Healthcare Patient Analytics Dashboard.pbix` in Power BI Desktop to view the Power BI report.
2. Open `Healthcare Patient Analytics Dashboard.twb` in Tableau Desktop to view the Tableau workbook.
3. Load `healthcare.csv` into Excel, Power BI, Tableau, or another analysis tool if you want to build on the dataset.

## Project Structure

```text
Healthcare-Patient-Analytics-Dashboard/
|-- dashboard.png
|-- dashboard2.png
|-- Healthcare Patient Analytics Dashboard.pbix
|-- Healthcare Patient Analytics Dashboard.twb
|-- healthcare.csv
`-- README.md
```

## Notes

- The dataset appears to be synthetic or anonymized patient data.
- Some analysis values are calculated inside the dashboard files rather than stored directly in the CSV.
