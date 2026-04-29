-- Overall Winner
SELECT
  source,
  ROUND(AVG(overall_score), 3) AS avg_score
FROM bizzy_bakeoff.gold.entity_scores
GROUP BY source
ORDER BY avg_score DESC;

-- Weak Fields
SELECT
  field_name,
  compared_source,
  ROUND(AVG(CASE WHEN winner = 'tie' THEN 1 ELSE 0 END), 3) AS match_rate
FROM bizzy_bakeoff.gold.field_comparisons
GROUP BY field_name, compared_source
ORDER BY match_rate ASC;

-- Coverage vs Accuracy
SELECT
  source,
  ROUND(AVG(coverage_score), 3) AS coverage,
  ROUND(AVG(accuracy_score), 3) AS accuracy
FROM bizzy_bakeoff.gold.entity_scores
GROUP BY source;