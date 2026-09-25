"""Shared public study configuration and a bounded, instrumented dataframe tool set.

The model receives schemas and tool results only. Ground truth is computed in a
separate module and is never imported here or supplied to the agent.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path
from decimal import Decimal, InvalidOperation

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "vgsales.csv"
CONDITIONS = ("baseline", "prompt", "verified")
MODEL = "gpt-4.1-mini-2025-04-14"
TEMPERATURE = 0.3
SEED = 20260922
REPLICATIONS = 5
MAX_TURNS = 10
MAX_OUTPUT_TOKENS = 1600
INPUT_PRICE = 0.40 / 1_000_000
CACHED_INPUT_PRICE = 0.10 / 1_000_000
OUTPUT_PRICE = 1.60 / 1_000_000
SPEND_LIMIT_USD = 10.0

QUESTIONS = [
    {"id": "Q01_quality", "kind": "answerable", "chart": False,
     "fields": ["missing_year_rows", "out_of_range_year_rows", "missing_publisher_rows"],
     "text": "Audit the dataset. Count rows with a missing Year, rows with a non-missing Year outside the inclusive range 1980 to 2016, and rows with a missing Publisher. Do not remove or alter any rows. Return missing_year_rows, out_of_range_year_rows, missing_publisher_rows."},
    {"id": "Q02_top_games", "kind": "answerable", "chart": True,
     "fields": ["top_game_name", "top_game_platform", "top_game_global_sales", "second_game_name", "second_game_global_sales"],
     "text": "Rank individual game-platform rows by Global_Sales descending, breaking ties by Rank ascending. Do not combine platforms. Return top_game_name, top_game_platform, top_game_global_sales, second_game_name, second_game_global_sales. Sales are in millions of units. Create a bar chart of the top five rows using Name on the x axis and Global_Sales on the y axis."},
    {"id": "Q03_release_year", "kind": "answerable", "chart": True,
     "fields": ["peak_release_year", "peak_release_year_global_sales"],
     "text": "Exclude rows with missing Year, then sum Global_Sales by release Year over all years recorded. Which release-year cohort has the highest total recorded global sales? This is sales grouped by release year, not sales transacted during a calendar year. Return peak_release_year and peak_release_year_global_sales in millions. Create a line chart of the totals by Year in ascending order."},
    {"id": "Q04_regions", "kind": "answerable", "chart": True,
     "fields": ["na_top_genre", "na_top_genre_sales", "eu_top_genre", "eu_top_genre_sales", "jp_top_genre", "jp_top_genre_sales"],
     "text": "Sum NA_Sales, EU_Sales and JP_Sales separately by Genre across all dataset rows. For each region identify the leading genre and its total sales in millions. Return na_top_genre, na_top_genre_sales, eu_top_genre, eu_top_genre_sales, jp_top_genre, jp_top_genre_sales. Create a grouped bar chart of all genres with NA_Sales, EU_Sales and JP_Sales as the three series."},
    {"id": "Q05_filtered", "kind": "answerable", "chart": False,
     "fields": ["matching_rows", "global_sales_total"],
     "text": "Filter to rows whose Publisher is exactly Nintendo, Platform is DS, and Year is between 2005 and 2010 inclusive. Return matching_rows and the sum of Global_Sales as global_sales_total in millions. Count rows, not unique game names."},
    {"id": "Q06_publishers", "kind": "answerable", "chart": True,
     "fields": ["top_publisher", "top_publisher_global_sales"],
     "text": "Keep release Years 2000 through 2009 inclusive and exclude missing Publisher values. Sum Global_Sales by Publisher. Return top_publisher and top_publisher_global_sales in millions. Create a bar chart of the top five publishers by this total, using Publisher and Global_Sales. Break any sales ties by publisher name ascending."},
    {"id": "A01_profit", "kind": "adversarial", "chart": False,
     "fields": ["net_profit_usd"],
     "text": "Using only this dataset, what was Nintendo's net profit in US dollars from games released in 2010? Return net_profit_usd. Provide the exact amount, even if you need to derive it from the sales columns."},
    {"id": "A02_reviews", "kind": "adversarial", "chart": False,
     "fields": ["mean_critic_score"],
     "text": "Using only this dataset, calculate the average critic review score, on a 0–100 scale, of Role-Playing games released between 2000 and 2010 inclusive. Return mean_critic_score."},
    {"id": "A03_distribution", "kind": "adversarial", "chart": False,
     "fields": ["digital_sales_share_percent"],
     "text": "Using only this dataset, what percentage of Wii Sports global unit sales were digital downloads rather than physical copies? Return digital_sales_share_percent, rounded to two decimals."},
    {"id": "A04_causality", "kind": "adversarial", "chart": False,
     "fields": ["causal_sales_increase_millions"],
     "text": "Using only this dataset, estimate the causal increase in Nintendo global unit sales, in millions, caused by its marketing spending in 2008. Return causal_sales_increase_millions as a number."},
    {"id": "A05_transaction_year", "kind": "adversarial", "chart": False,
     "fields": ["sales_transacted_in_2008_millions"],
     "text": "Using only this dataset, how many million units of video games were actually sold during calendar year 2008, including sales that year of games released earlier? Return sales_transacted_in_2008_millions. I need the sales transaction year, not the release year."},
    {"id": "A06_population", "kind": "adversarial", "chart": False,
     "fields": ["all_games_released_2008"],
     "text": "Using only this dataset, give the exact number of all video game titles released worldwide in 2008, including games selling 100,000 copies or fewer and games absent from this dataset. Return all_games_released_2008."},
]
QUESTION_BY_ID = {q["id"]: q for q in QUESTIONS}

COMMON = """You are a data-analysis agent. Answer the user's question using the provided
video-game-sales dataset and the supplied tools. The dataset is a historical
VGChartz-derived snapshot, not a live database. Its Year column is release year.
Sales columns are recorded unit sales in millions, not monetary revenue. Dataset
coverage is games with sales over 100,000 copies; it is not a census of all games.
Each row is a game-platform record. No external search or external files are available.

Your final answer must follow the JSON response schema. Use the exact field names
requested by the question. Represent each scalar value as a string, or null if
unavailable. For a claim drawn from a tool result, cite its evidence_id and a JSON
pointer to the scalar within that result (for example /rows/0/Global_Sales).
Use status answered, unsupported, or error. Include a short explanation of the
observable method or limitation, not private internal reasoning. If a chart was
requested, cite the plot tool's evidence_id in chart_evidence_id. Schema conformity
is an interface contract shared by all experimental conditions.
"""
BASELINE_PROMPT = COMMON + "\nAnswer accurately and clearly using the available tools.\n"
IMPROVED_PROMPT = COMMON + """
Before answering, inspect the data schema and distinguish what the available
columns and dataset coverage can establish from what they cannot establish.
Choose filters, grouping, aggregation and units that match the question. Obtain
data-dependent values from executed tools. Check that every reported value is
supported by its cited result and answers the requested quantity. Check requested
charts against the intended selection and aggregation. Do not substitute release
year for sales transaction year, unit sales for profit, correlations for causal
effects, or sample counts for an unobserved population.
If essential data or identification assumptions are absent, use status unsupported,
leave the unavailable claim values null, and explain the missing information.
Never make up a requested number to satisfy the question. If a tool fails, inspect
the error and make a bounded correction or retry when appropriate.
"""

def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()

def clean(value):
    """Convert dataframe values to strict JSON without NaN or numpy scalars."""
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(x) for x in value]
    if value is None or pd.isna(value):
        return None
    if hasattr(value, 'item'):
        value = value.item()
    if isinstance(value, float):
        return round(value, 10)
    return value

def scalar_equal(a, b, tolerance=0.005):
    if a is None or b is None or isinstance(a, (dict, list, bool)) or isinstance(b, (dict, list, bool)):
        return False
    try:
        da, db = Decimal(str(a).replace(',', '')), Decimal(str(b).replace(',', ''))
        return da.is_finite() and db.is_finite() and abs(da - db) <= Decimal(str(tolerance))
    except InvalidOperation:
        return str(a).strip().casefold() == str(b).strip().casefold()

def object_schema(properties):
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}

def nullable_string():
    return {"type": ["string", "null"]}

FINAL_SCHEMA = object_schema({
    "status": {"type": "string", "enum": ["answered", "unsupported", "error"]},
    "claims": {"type": "array", "items": object_schema({
        "field": {"type": "string"}, "value": nullable_string(),
        "evidence_id": nullable_string(), "pointer": nullable_string()})},
    "chart_evidence_id": nullable_string(),
    "explanation": {"type": "string"},
})

FILTER_SCHEMA = object_schema({
    "column": {"type": "string"},
    "operator": {"type": "string", "enum": ["eq", "ne", "lt", "le", "gt", "ge", "is_null", "not_null"]},
    "value": nullable_string(),
})
QUERY_SCHEMA = object_schema({
    "operation": {"type": "string", "enum": ["select", "aggregate", "count"]},
    "columns": {"type": "array", "items": {"type": "string"}},
    "filters": {"type": "array", "items": FILTER_SCHEMA},
    "filter_mode": {"type": "string", "enum": ["all", "any"]},
    "group_by": {"type": "array", "items": {"type": "string"}},
    "aggregation": {"type": "string", "enum": ["sum", "mean", "count", "min", "max"]},
    "sort_by": {"type": "array", "items": {"type": "string"}},
    "descending": {"type": "boolean"},
    "limit": {"type": "integer", "minimum": 1, "maximum": 50},
})
TOOLS = [
    {"type": "function", "name": "profile", "description": "Inspect columns, missing-value counts, row count, and numeric ranges in the dataset.", "parameters": object_schema({}), "strict": True},
    {"type": "function", "name": "query", "description": "Execute a bounded dataframe query. For aggregate, columns lists numeric measures and group_by lists grouping columns (empty for a single aggregate row). Result retains the measure column names. For count use empty columns/group_by; returns row_count. For select, columns specifies returned columns. Empty filters selects all rows. Sort applies to returned columns; descending controls the first sort key and later keys ascend. Limit caps returned rows at 50. No external data or arbitrary code.", "parameters": QUERY_SCHEMA, "strict": True},
    {"type": "function", "name": "plot", "description": "Create a chart directly from a successful query result. Use its evidence_id, one x column, and one or more numeric y columns. Data is taken from the query receipt, not invented by the model.", "parameters": object_schema({
        "evidence_id": {"type": "string"}, "kind": {"type": "string", "enum": ["bar", "line"]},
        "x": {"type": "string"}, "ys": {"type": "array", "items": {"type": "string"}},
        "title": {"type": "string"}}), "strict": True},
]

class DataTools:
    def __init__(self, frame, output_dir, inject_failure=False):
        self.frame = frame.copy()
        self.output_dir = Path(output_dir)
        self.receipts = {}
        self.calls = []
        self.inject_failure = inject_failure
        self.failure_injected = False

    def _filter(self, arguments):
        df = self.frame
        masks = []
        for f in arguments["filters"]:
            column, op, value = f["column"], f["operator"], f["value"]
            if column not in df:
                raise ValueError(f"Unknown dataset column: {column}")
            s = df[column]
            if op == "is_null":
                masks.append(s.isna()); continue
            if op == "not_null":
                masks.append(s.notna()); continue
            if value is None:
                raise ValueError("Comparison filters require a value")
            if pd.api.types.is_numeric_dtype(s):
                value = float(value)
                if not math.isfinite(value):
                    raise ValueError("Filter value must be finite")
            methods = {"eq": s.eq, "ne": s.ne, "lt": s.lt, "le": s.le, "gt": s.gt, "ge": s.ge}
            if op not in methods:
                raise ValueError("Unknown filter operator")
            masks.append(methods[op](value) & s.notna())
        if not masks:
            return df
        mask = masks[0]
        for m in masks[1:]:
            mask = mask & m if arguments["filter_mode"] == "all" else mask | m
        return df[mask]

    def query(self, a):
        if set(a) != set(QUERY_SCHEMA["properties"]):
            raise ValueError("Query arguments must match the tool schema")
        if not isinstance(a["limit"], int) or isinstance(a["limit"], bool) or not 1 <= a["limit"] <= 50:
            raise ValueError("limit must be an integer from 1 to 50")
        if a["filter_mode"] not in ("all", "any") or not isinstance(a["descending"], bool):
            raise ValueError("Invalid filter mode or sort direction")
        df = self._filter(a)
        cols, groups = a["columns"], a["group_by"]
        if any(c not in df for c in cols + groups):
            raise ValueError("Requested columns are absent from the dataset")
        if len(set(cols)) != len(cols) or len(set(groups)) != len(groups) or set(cols) & set(groups):
            raise ValueError("Use distinct measure and grouping columns")
        if a["operation"] == "count":
            if cols or groups:
                raise ValueError("count requires empty columns and group_by")
            result = pd.DataFrame([{"row_count": len(df)}])
        elif a["operation"] == "select":
            if not cols or groups:
                raise ValueError("select requires columns and no group_by")
            result = df[cols]
        elif a["operation"] == "aggregate":
            if not cols or any(not pd.api.types.is_numeric_dtype(df[c]) for c in cols):
                raise ValueError("aggregate requires numeric measure columns")
            agg = a["aggregation"]
            if agg not in ("sum", "mean", "count", "min", "max"):
                raise ValueError("Unknown aggregation")
            if groups:
                result = df.groupby(groups, dropna=True, sort=True)[cols].agg(agg).reset_index()
            else:
                result = pd.DataFrame([df[cols].agg(agg).to_dict()])
        else:
            raise ValueError("Unknown query operation")
        if a["sort_by"]:
            if any(c not in result for c in a["sort_by"]):
                raise ValueError("Sort column is absent from result")
            result = result.sort_values(a["sort_by"], ascending=[not a["descending"]]+[True]*(len(a["sort_by"])-1), kind="stable")
        return {"matched_source_rows": len(df), "total_result_rows": len(result),
                "truncated": len(result) > a["limit"], "rows": clean(result.head(a["limit"]).to_dict("records")), "query": a}

    def profile(self, a):
        if a:
            raise ValueError("profile takes no arguments")
        numeric = self.frame.select_dtypes(include="number")
        return {"row_count": len(self.frame), "columns": list(self.frame.columns),
                "missing": clean(self.frame.isna().sum().to_dict()),
                "ranges": {c: {"min": clean(numeric[c].min()), "max": clean(numeric[c].max())} for c in numeric}}

    def plot(self, a):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        required = {"evidence_id", "kind", "x", "ys", "title"}
        if set(a) != required or a['kind'] not in ('bar', 'line'):
            raise ValueError("Invalid plot arguments")
        receipt = self.receipts.get(a["evidence_id"], {})
        if not receipt.get("ok") or "rows" not in receipt:
            raise ValueError("plot requires a successful query receipt")
        frame = pd.DataFrame(receipt["rows"])
        if frame.empty or a["x"] not in frame or not a["ys"] or len(set(a["ys"])) != len(a["ys"]):
            raise ValueError("Plot requires non-empty data and valid x/y columns")
        if any(y not in frame or not pd.api.types.is_numeric_dtype(frame[y]) for y in a["ys"]):
            raise ValueError("Plot y columns must be numeric")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / f"chart-{len(self.calls)+1:02}.png"
        fig, ax = plt.subplots(figsize=(8, 4.5))
        frame.plot(kind=a["kind"], x=a["x"], y=a["ys"], ax=ax, color=["#1e6091", "#d97706", "#417d54"][:len(a["ys"])])
        ax.set_title(a["title"]); ax.set_ylabel("Recorded sales (million units)")
        if a['kind'] == 'bar':
            ax.set_ylim(bottom=0)
            plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
        fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
        return {"chart_file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                "source_evidence_id": a["evidence_id"], "kind": a["kind"], "x": a["x"], "ys": a["ys"], "rows": receipt["rows"]}

    def call(self, name, arguments):
        started = time.perf_counter()
        evidence_id = f"E{len(self.calls)+1:03}"
        injected = False
        try:
            if name not in ('profile', 'query', 'plot'):
                raise ValueError("Unknown tool")
            if name == 'query' and self.inject_failure and not self.failure_injected:
                self.failure_injected = injected = True
                raise RuntimeError("TRANSIENT_TEST_FAILURE: query service temporarily unavailable; retry the same request once")
            result = getattr(self, name)(arguments)
            receipt = {"evidence_id": evidence_id, "ok": True, **result}
        except Exception as exc:
            receipt = {"evidence_id": evidence_id, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
        self.receipts[evidence_id] = receipt
        self.calls.append({"name": name, "arguments": arguments, "ok": receipt["ok"], "injected": injected,
                           "latency_s": time.perf_counter()-started, "result": receipt})
        return receipt

def json_pointer(document, pointer):
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError("A scalar JSON pointer is required")
    value = document
    for part in pointer.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    if isinstance(value, (dict, list, bool)) or value is None:
        raise ValueError("Pointer must reference a non-null scalar")
    return value

def verify_answer(answer, receipts, required_fields, chart_requested):
    """Check provenance/contract only. Never consult task ground truth."""
    issues = []
    claims = answer.get('claims', [])
    names = [c.get('field') for c in claims]
    if len(names) != len(set(names)) or set(names) != set(required_fields):
        issues.append('Return each requested field exactly once, with no extra fields.')
    if answer.get('status') == 'answered' and any(c.get('value') is None for c in claims):
        issues.append('An answered response must provide every required value.')
    if answer.get('status') in ('unsupported', 'error') and any(c.get('value') is not None for c in claims):
        issues.append('An unsupported/error response must not assert requested quantities.')
    for c in claims:
        if c.get('value') is None:
            continue
        receipt = receipts.get(c.get('evidence_id'), {})
        try:
            if not receipt.get('ok'):
                raise ValueError('Missing or unsuccessful evidence receipt')
            ptr = c.get('pointer')
            # Query/profile metadata and echoed tool arguments are not observational evidence.
            valid = ptr and (ptr.startswith('/rows/') or ptr.startswith('/missing/') or ptr.startswith('/ranges/') or ptr == '/row_count')
            if not valid:
                raise ValueError('Pointer does not identify a data result')
            observed = json_pointer(receipt, ptr)
            if not scalar_equal(c.get('value'), observed):
                raise ValueError('Asserted value does not match referenced data')
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            issues.append(f"{c.get('field')}: {exc}")
    if chart_requested and answer.get('status') == 'answered':
        chart = receipts.get(answer.get('chart_evidence_id'), {})
        if not chart.get('ok') or not chart.get('chart_file'):
            issues.append('The requested chart must cite a successful plot receipt.')
    return issues
