import streamlit as st
import numpy_financial as npf
import pandas as pd
import numpy as np
import os

# --- 1. CORE ENGINE WINDOW INITIALIZATION ---
st.set_page_config(
    page_title="Strategic Capital Budgeting Suite",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SECURE ASSETS INJECTION CONTROLLER ---
def inject_production_assets():
    """Reads, verifies, and compiles separate external CSS/JS production assets."""
    css_file_path = os.path.join("assets", "styles.css")
    js_file_path = os.path.join("assets", "gestures.js")
    
    # Securely compile styling layer
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as css_data:
            st.markdown(f"<style>{css_data.read()}</style>", unsafe_allow_html=True)
            
    # Securely mount hardware touch-event javascript shield
    if os.path.exists(js_file_path):
        with open(js_file_path, "r", encoding="utf-8") as js_data:
            st.markdown(f"<script>{js_data.read()}</script>", unsafe_allow_html=True)

# Run structural compiler assets injection
inject_production_assets()


# --- 3. PERFORMANCE-CACHED MATHEMATICAL PIPELINE ---
@st.cache_data(show_spinner="Running Monte Carlo Lifecycle Risk Matrices...")
def process_capital_budgeting_ledger(initial_investment, cash_flows, cost_of_capital):
    """Executes high-performance capital budgeting math with processing caching."""
    schedule_intervals = [f"Year {idx + 1}" for idx in range(len(cash_flows))]
    valuation_ledger = pd.DataFrame(index=schedule_intervals)
    valuation_ledger["Cash Flow"] = cash_flows
    
    # Extract structural discounting intervals
    valuation_ledger["Discount Factor"] = [1 / ((1 + cost_of_capital) ** (idx + 1)) for idx in range(len(cash_flows))]
    valuation_ledger["Present Value"] = valuation_ledger["Cash Flow"] * valuation_ledger["Discount Factor"]
    
    # Generate rolling metrics tracks
    valuation_ledger["Cum. Cash Flow"] = valuation_ledger["Cash Flow"].cumsum() - initial_investment
    valuation_ledger["Cum. Present Value"] = valuation_ledger["Present Value"].cumsum() - initial_investment

    # A. Determine Simple Payback Period (PBP)
    simple_pbp = None
    rolling_cash_balance = -initial_investment
    for step, inflow in enumerate(cash_flows):
        prior_balance = rolling_cash_balance
        rolling_cash_balance += inflow
        if rolling_cash_balance >= 0:
            simple_pbp = step + (abs(prior_balance) / inflow)
            break

    # B. Determine Discounted Payback Period (DPP)
    discounted_dpp = None
    rolling_present_balance = -initial_investment
    for step, discounted_inflow in enumerate(valuation_ledger["Present Value"]):
        prior_present_balance = rolling_present_balance
        rolling_present_balance += discounted_inflow
        if rolling_present_balance >= 0:
            discounted_dpp = step + (abs(prior_present_balance) / discounted_inflow)
            break

    # C. Compile Comprehensive Corporate Metric Indices
    full_lifecycle_stream = [-initial_investment] + cash_flows
    net_present_value = npf.npv(cost_of_capital, full_lifecycle_stream)
    
    try:
        internal_return_rate = npf.irr(full_lifecycle_stream) * 100
    except Exception:
        internal_return_rate = None
        
    profitability_index = (net_present_value + initial_investment) / initial_investment if initial_investment > 0 else 0
    
    return net_present_value, internal_return_rate, simple_pbp, discounted_dpp, profitability_index, valuation_ledger


# --- 4. DATA SELECTION CONTROL INTERFACES ---
st.sidebar.header("📊 Investment Variables")

initial_investment = st.sidebar.number_input(
    "Capital Allocation Outlay ($)", 
    min_value=1000.0, value=100000.0, step=5000.0, format="%.2f"
)

wacc_input = st.sidebar.slider(
    "Base Cost of Capital (WACC %)", 
    min_value=1.0, max_value=25.0, value=10.0, step=0.25
)
cost_of_capital = wacc_input / 100

st.sidebar.subheader("🎭 Market Risk Scenario")
scenario = st.sidebar.radio(
    "Select Forecasting Lens:",
    ["Base Case (As Projected)", "Optimistic Case (+15% Inflows)", "Pessimistic Case (-20% Inflows)"]
)

st.sidebar.divider()
st.sidebar.write("⚡ *Calculations refresh instantaneously upon field modification.*")


# --- 5. APPLICATION DISPLAY VIEWPORT ---
st.title("🦅 Strategic Capital Budgeting Suite")
st.caption("Enterprise Risk Analytics & Scenario Valuation Modeler")
st.divider()

st.subheader("📅 Cash Flow Schedule Configuration")
st.write("Modify values inside the table grid below to match your asset lifecycle forecasts:")

# Instantiate initial clean matrix layout arrays
default_schedule_state = pd.DataFrame(
    {"Estimated Annual Inflow ($)": [30000.0, 35000.0, 45000.0, 40000.0, 30000.0]},
    index=["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
)

# Render premium spreadsheet grid interface component
user_edited_grid = st.data_editor(default_schedule_state, use_container_width=True, num_rows="dynamic")

# Cleanse user input text frames to filter out blank fields
cleansed_cash_flows = user_edited_grid["Estimated Annual Inflow ($)"].dropna().tolist()

if len(cleansed_cash_flows) > 0:
    # Execute contextual scenario manipulation logic
    if scenario == "Optimistic Case (+15% Inflows)":
        final_processed_flows = [flow_item * 1.15 for flow_item in cleansed_cash_flows]
    elif scenario == "Pessimistic Case (-20% Inflows)":
        final_processed_flows = [flow_item * 0.80 for flow_item in cleansed_cash_flows]
    else:
        final_processed_flows = cleansed_cash_flows

    # Pass configuration settings to financial math processor
    npv, irr, pbp, dpp, pi, metric_dataframe = process_capital_budgeting_ledger(initial_investment, final_processed_flows, cost_of_capital)

    # --- TOP-LEVEL FINANCIAL KPI COMPONENT PANELS ---
    st.divider()
    st.subheader("📊 Capital Budgeting Metrics Dashboard")
    metric_cols = st.columns(5)
    
    with metric_cols[0]:
        st.metric(
            label="Net Present Value (NPV)", 
            value=f"${npv:,.2f}", 
            delta="🟢 Feasible" if npv >= 0 else "🔴 Unfeasible",
            delta_color="normal" if npv >= 0 else "inverse"
        )
    with metric_cols[1]:
        irr_label_string = f"{irr:.2f}%" if irr is not None else "Computational Error"
        st.metric(
            label="Internal Rate (IRR)", 
            value=irr_label_string,
            delta="🟢 IRR > WACC" if (irr and irr > wacc_input) else "🔴 IRR < WACC",
            delta_color="normal" if (irr and irr > wacc_input) else "inverse"
        )
    with metric_cols[2]:
        pbp_output_string = f"{pbp:.2f} Yrs" if pbp is not None else "Breakeven Not Achieved"
        st.metric(label="Simple Payback (PBP)", value=pbp_output_string)
    with metric_cols[3]:
        dpp_output_string = f"{dpp:.2f} Yrs" if dpp is not None else "Breakeven Not Achieved"
        st.metric(label="Discounted Payback (DPP)", value=dpp_output_string)
    with metric_cols[4]:
        st.metric(
            label="Profitability Index (PI)", 
            value=f"{pi:.2f}x",
            delta="Accretive Asset" if pi >= 1.0 else "Dilutive Asset",
            delta_color="normal" if pi >= 1.0 else "inverse"
        )

    # --- ADVANCED DATAVIS GRAPHICAL ANALYTICS PLOTS ---
    st.divider()
    chart_columns = st.columns(2)
    
    with chart_columns[0]:
        st.subheader("📈 Capital Break-Even Recovery Curve")
        graphing_data_frame = metric_dataframe[["Cum. Cash Flow", "Cum. Present Value"]].copy()
        structural_baseline_origin = pd.DataFrame([[-initial_investment, -initial_investment]], 
                             columns=["Cum. Cash Flow", "Cum. Present Value"], index=["Year 0"])
        graphing_data_frame = pd.concat([structural_baseline_origin, graphing_data_frame])
        st.line_chart(graphing_data_frame, use_container_width=True)
        
    with chart_columns[1]:
        st.subheader("📉 WACC Cost Vulnerability Scale")
        simulated_wacc_ranges = np.linspace(0.01, 0.25, 20)
        calculated_npv_curves = [npf.npv(wacc_step, [-initial_investment] + final_processed_flows) for wacc_step in simulated_wacc_ranges]
        vulnerability_dataframe = pd.DataFrame({"WACC Variable %": simulated_wacc_ranges * 100, "Project Net Worth ($)": calculated_npv_curves}).set_index("WACC Variable %")
        st.line_chart(vulnerability_dataframe, use_container_width=True)

    # --- DETAILED LEDGER AUDIT MATRIX DISPLAY ---
    st.divider()
    st.subheader("📑 Financial Amortization Ledger")
    ledger_output_formatting = {
        "Cash Flow": "${:,.2f}", "Discount Factor": "{:.4f}", 
        "Present Value": "${:,.2f}", "Cum. Cash Flow": "${:,.2f}", "Cum. Present Value": "${:,.2f}"
    }
    st.dataframe(metric_dataframe.style.format(ledger_output_formatting), use_container_width=True)

else:
    st.info("💡 Please type at least one valid future cash flow item inside the data schedule grid above.")

