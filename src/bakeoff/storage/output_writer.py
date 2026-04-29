from pathlib import Path

import pandas as pd
from pydantic import BaseModel

from bakeoff.config import BakeoffConfig
from bakeoff.storage.delta_writer import write_delta_table


def records_to_dataframe(records: list[BaseModel]) -> pd.DataFrame:
    return pd.DataFrame([record.model_dump(mode="json") for record in records])


def write_outputs(
    config: BakeoffConfig,
    field_comparisons: list[BaseModel],
    entity_scores: list[BaseModel],
) -> None:
    if config.output_mode == "csv":
        write_csv_outputs(config, field_comparisons, entity_scores)
    elif config.output_mode == "delta":
        write_delta_outputs(config, field_comparisons, entity_scores)
    else:
        raise ValueError(f"Unsupported output mode: {config.output_mode}")


def write_csv_outputs(
    config: BakeoffConfig,
    field_comparisons: list[BaseModel],
    entity_scores: list[BaseModel],
) -> None:
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    comparisons_df = records_to_dataframe(field_comparisons)
    scores_df = records_to_dataframe(entity_scores)

    comparisons_df.to_csv(output_dir / "field_comparisons.csv", index=False)
    scores_df.to_csv(output_dir / "entity_scores.csv", index=False)

    summary_df = (
        scores_df.groupby(["entity_type", "source"], as_index=False)
        .agg(
            records=("entity_id", "count"),
            avg_accuracy_score=("accuracy_score", "mean"),
            avg_coverage_score=("coverage_score", "mean"),
            avg_freshness_score=("freshness_score", "mean"),
            avg_format_score=("format_score", "mean"),
            avg_overall_score=("overall_score", "mean"),
        )
    )

    summary_df.to_csv(output_dir / "executive_summary.csv", index=False)
    
def write_delta_outputs(
    config: BakeoffConfig,
    field_comparisons,
    entity_scores,
):
    comparisons_df = records_to_dataframe(field_comparisons)
    scores_df = records_to_dataframe(entity_scores)

    write_delta_table(comparisons_df, "field_comparisons", config)
    write_delta_table(scores_df, "entity_scores", config)

    summary_df = (
        scores_df.groupby(["entity_type", "source"], as_index=False)
        .agg(
            records=("entity_id", "count"),
            avg_accuracy_score=("accuracy_score", "mean"),
            avg_coverage_score=("coverage_score", "mean"),
            avg_freshness_score=("freshness_score", "mean"),
            avg_format_score=("format_score", "mean"),
            avg_overall_score=("overall_score", "mean"),
        )
    )

    write_delta_table(summary_df, "executive_summary", config)