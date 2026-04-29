-- Overall Winner
SELECT
  source,
  ROUND(AVG(overall_score), 3) AS avg_overall_score,
  ROUND(AVG(accuracy_score), 3) AS avg_accuracy_score,
  ROUND(AVG(coverage_score), 3) AS avg_coverage_score,
  ROUND(AVG(freshness_score), 3) AS avg_freshness_score
FROM bizzy_bakeoff.gold.entity_scores
GROUP BY source
ORDER BY avg_overall_score DESC;

-- Weak Fields
SELECT
  entity_type,
  field_name,
  compared_source,
  COUNT(*) AS compared_values,
  SUM(CASE WHEN winner != 'tie' THEN 1 ELSE 0 END) AS disagreements,
  ROUND(
    SUM(CASE WHEN winner != 'tie' THEN 1 ELSE 0 END) / COUNT(*),
    3
  ) AS disagreement_rate
FROM bizzy_bakeoff.gold.field_comparisons
GROUP BY entity_type, field_name, compared_source
ORDER BY disagreement_rate DESC;

-- Coverage vs Accuracy
SELECT
  source,
  ROUND(AVG(coverage_score), 3) AS coverage,
  ROUND(AVG(accuracy_score), 3) AS accuracy
FROM bizzy_bakeoff.gold.entity_scores
GROUP BY source;