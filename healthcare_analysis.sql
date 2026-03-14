-- Table view
SELECT * 
FROM healthcare limit 10;

-- Total Number of Patients
SELECT COUNT(*) AS total_patients
FROM healthcare;

SELECT gender, COUNT(*) AS patient_count
FROM healthcare
GROUP BY gender;

-- Average Billing Amount
SELECT AVG(billing_amount) AS avg_bill
FROM healthcare;

-- Most Common Medical Condition
SELECT medical_condition, COUNT(*) AS cases
FROM healthcare
GROUP BY medical_condition
ORDER BY cases DESC;

-- Patients per Hospital
SELECT hospital, COUNT(*) AS total_patients
FROM healthcare
GROUP BY hospital
ORDER BY total_patients DESC;

-- Insurance Provider Analysis
SELECT insurance_provider, COUNT(*) AS patients
FROM healthcare
GROUP BY insurance_provider
ORDER BY patients DESC;

-- Average Billing by Condition
SELECT medical_condition, AVG(billing_amount) AS avg_bill
FROM healthcare
GROUP BY medical_condition
ORDER BY avg_bill DESC;

-- Top 5 Hospitals by billing_amount
SELECT hospital, SUM(billing_amount) AS total_revenue
FROM healthcare
GROUP BY hospital
ORDER BY total_revenue DESC
LIMIT 5;

