# qc-data-processor

## Overview
QC Data Processor is an MCP Server that provides quality control data analysis tools. It can parse QC data, perform SPC analysis (control charts, process capability), reliability analysis (Weibull/Lognormal fitting), and generate QC reports in Markdown format.

## When to Use
- User asks to analyze quality control data (SPC charts, process capability)
- User asks to perform reliability/Weibull analysis on life test data
- User asks to generate QC reports (daily, weekly, 8D, reliability)
- User mentions SPC, Cp/Cpk, control charts, Weibull, MTTF, B10 life
- User provides Excel/CSV files with measurement, time-to-failure, or pass/fail data

## Trigger Keywords
SPC, 控制图, 过程能力, Cp, Cpk, 良率, Weibull, 可靠性, 寿命, MTTF, B10, 8D, 品质报告, 日报, 周报, 客诉, QC

## Tools

### 1. qc_parse_data_tool
Parse QC data file (CSV/Excel) and auto-detect column types, pipeline, and control chart suggestions.

**Input:**
- `file_path` (str): Path to data file (.csv, .xlsx, .xls)
- `mode` (str, optional): "auto" by default

**Output:** JSON schema with column types, pipeline detection, and chart suggestions.

### 2. qc_spc_analyze_tool
Perform SPC analysis: control charts (Xbar-R, I-MR), capability indices (Cp, Cpk, Pp, Ppk), Western Electric rules.

**Input:**
- `data_schema` (dict): Output from qc_parse_data_tool (must include `_file_path`)
- `column` (str): Measurement column name
- `subgroup_size` (int, optional): Subgroup size
- `chart_type` (str, optional): "Xbar-R", "I-MR", or "auto"

**Output:** Statistics (control limits, capability indices), alarms, chart data.

### 3. qc_reliability_analyze_tool
Fit reliability distributions (Weibull, Lognormal, Exponential) using MLE, select best via AICc.

**Input:**
- `data_schema` (dict): Output from qc_parse_data_tool (must include `_file_path`)
- `time_column` (str): Column containing time-to-failure data
- `censor_column` (str): Column containing censor indicators (1=failure, 0=censored)
- `distribution` (str, optional): "auto" (try all), "Weibull", "Lognormal", or "Exponential"

**Output:** Best-fit distribution, parameters with CI, B10/B50/MTTF, probability plot data.

### 4. qc_report_generate_tool
Generate QC reports in Markdown format.

**Input:**
- `analysis_result` (dict): Output from SPC or reliability analysis
- `template` (str): One of "daily", "weekly", "8d", "reliability"
- `metadata` (dict): Product name, date, customer, etc.

**Output:** Markdown string.

## MCP Configuration

```json
{
  "mcpServers": {
    "qc-data-processor": {
      "command": "python",
      "args": ["path/to/mcp_server.py"],
      "env": {}
    }
  }
}
```

## Dependencies
```
mcp>=1.0.0
pandas>=2.0.0
openpyxl>=3.0.0
numpy>=1.24.0
scipy>=1.10.0
reliability>=0.8.0
```

## Example Usage

### Parse and SPC analysis
```
User: Analyze the SPC data in data/spc_sample.csv

1. qc_parse_data_tool("data/spc_sample.csv") -> schema
2. qc_spc_analyze_tool(schema, "measurement") -> spc_result
3. qc_report_generate_tool(spc_result, "daily", {"product": "Widget"})
```

### Reliability analysis
```
User: Run Weibull analysis on data/reliability_sample.csv with time column "time" and censor column "censor"

1. qc_parse_data_tool("data/reliability_sample.csv") -> schema
2. qc_reliability_analyze_tool(schema, "time", "censor") -> rel_result
3. qc_report_generate_tool(rel_result, "reliability", {"product": "Widget"})
```

## Notes
- All outputs are text/JSON, no images or GUI
- Uses stdio transport, no API keys required
- Process capability formulas match Minitab/JMP standard methods
- Control chart constants (A2, D3, D4, d2) for n=2~25
