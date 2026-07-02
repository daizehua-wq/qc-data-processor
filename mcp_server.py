from mcp.server.fastmcp import FastMCP
from tools.parse_data import qc_parse_data
from tools.spc_analyze import qc_spc_analyze
from tools.reliability_analyze import qc_reliability_analyze
from tools.report_generate import qc_report_generate

mcp = FastMCP("QC Tool")


@mcp.tool()
def qc_parse_data_tool(file_path: str, mode: str = "auto") -> dict:
    """Parse quality control data from Excel/CSV file. Auto-detects column types, pipeline (SPC/reliability), and suggests control charts."""
    return qc_parse_data(file_path, mode)


@mcp.tool()
def qc_spc_analyze_tool(data_schema: dict, column: str, subgroup_size: int = None, chart_type: str = "auto") -> dict:
    """Perform SPC analysis: control charts (Xbar-R, I-MR), capability indices (Cp, Cpk, Pp, Ppk), and 8 Western Electric alarm rules."""
    return qc_spc_analyze(data_schema, column, subgroup_size, chart_type)


@mcp.tool()
def qc_reliability_analyze_tool(data_schema: dict, time_column: str, censor_column: str, distribution: str = "auto") -> dict:
    """Perform reliability analysis: Weibull/Lognormal/Exponential fitting, AICc selection, B10/B50/MTTF computation."""
    return qc_reliability_analyze(data_schema, time_column, censor_column, distribution)


@mcp.tool()
def qc_report_generate_tool(analysis_result: dict, template: str, metadata: dict = None) -> str:
    """Generate QC report (daily/weekly/8d/reliability) in Markdown format with ASCII charts."""
    return qc_report_generate(analysis_result, template, metadata)


if __name__ == "__main__":
    mcp.run()
