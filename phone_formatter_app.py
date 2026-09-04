import streamlit as st
import pandas as pd
import re
import io
import base64

st.set_page_config(page_title="Vierra Property Broker | Phone Formatter", page_icon="\U0001F4DE", layout="centered")

# ---------------------------------------------------------------------------
# Brand assets & theme (Vierra Property Broker)
# ---------------------------------------------------------------------------
LOGO_B64 = "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"

BRAND_CHARCOAL = "#333333"
BRAND_ORANGE = "#F7941D"
BRAND_LIGHT_GRAY = "#F5F5F5"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: #FFFFFF;
        }}
        h1, h2, h3 {{
            color: {BRAND_CHARCOAL} !important;
            font-family: 'Trebuchet MS', sans-serif;
        }}
        .vierra-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 18px;
            padding: 10px 0 6px 0;
        }}
        .vierra-header img {{
            height: 64px;
        }}
        .vierra-tagline {{
            text-align: center;
            color: {BRAND_CHARCOAL};
            font-size: 0.95rem;
            letter-spacing: 0.5px;
            margin-top: -6px;
            margin-bottom: 18px;
        }}
        .vierra-divider {{
            border: none;
            border-top: 3px solid {BRAND_ORANGE};
            width: 80px;
            margin: 0 auto 24px auto;
        }}
        div.stButton > button, div.stDownloadButton > button {{
            background-color: {BRAND_ORANGE};
            color: white;
            border: none;
            font-weight: 600;
        }}
        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            background-color: #d97c11;
            color: white;
        }}
        .stAlert {{
            border-left: 4px solid {BRAND_ORANGE};
        }}
        section[data-testid="stFileUploaderDropzone"] {{
            border: 2px dashed {BRAND_ORANGE} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="vierra-header">
        <img src="data:image/png;base64,{LOGO_B64}" alt="Vierra Property Broker logo" />
    </div>
    <div class="vierra-tagline">UAE PHONE NUMBER FORMATTER</div>
    <hr class="vierra-divider" />
    """,
    unsafe_allow_html=True,
)

st.write(
    "Upload an Excel or CSV file, pick the phone number column, and this app will clean "
    "and reformat every number to the **+971XXXXXXXXX** format \u2014 even messy ones that "
    "Excel has turned into scientific notation or decimals (e.g. `9.71501E+11`, "
    "`971501234567.0`, `97.1501234567`)."
)


def _repair_excel_mangled_number(s: str) -> str:
    """
    Excel/CSV often silently converts long phone numbers into scientific
    notation or floats, e.g.:
        971501234567      -> 9.71501234567E+11   or   971501234567.0
    This corrupts naive digit-stripping (the 'E+11' or '.0' get merged
    into the digit string in the wrong order/length). Detect these
    patterns and repair them back into a plain integer string BEFORE
    the normal digit-cleaning pass runs.
    """
    s = s.strip()

    # Scientific notation: 9.71501234567E+11 / 9.71501234567e11 / etc.
    if re.fullmatch(r"[+-]?\d+(\.\d+)?[eE][+-]?\d+", s):
        try:
            value = float(s)
            # Round to nearest whole number - phone numbers have no
            # fractional part, so this recovers the true digit sequence
            # as long as the exponent didn't already lose precision.
            return str(int(round(value)))
        except (ValueError, OverflowError):
            return s

    # Plain float that should be a whole number: 971501234567.0
    if re.fullmatch(r"[+-]?\d+\.0+", s):
        try:
            return str(int(round(float(s))))
        except ValueError:
            return s

    # Excel dropped a leading zero and inserted a stray decimal point in
    # the middle, e.g. "97.1501234567" (should be 971501234567). Any
    # decimal point that is NOT part of a genuine float-looking pattern
    # is just noise from a badly formatted cell - strip it and keep the
    # digits in their original left-to-right order.
    if "." in s and re.fullmatch(r"[+\d.\s-]+", s):
        collapsed = s.replace(".", "")
        if collapsed.isdigit() or (collapsed.startswith("+") and collapsed[1:].isdigit()):
            return collapsed

    return s


def clean_and_format_number(raw_value: str) -> str:
    """
    Clean a raw phone number string and reformat it to +971XXXXXXXXX.

    Handles cases like:
      050 123 4567       -> +971501234567
      0501234567          -> +971501234567
      501234567           -> +971501234567
      971501234567        -> +971501234567
      00971501234567      -> +971501234567
      +971 50 123 4567    -> +971501234567
      9.71501234567E+11   -> +971501234567   (Excel scientific notation)
      971501234567.0      -> +971501234567   (Excel float export)
      97.1501234567       -> +971501234567   (stray decimal / dropped 0)
    """
    if raw_value is None:
        return ""

    s = str(raw_value).strip()
    if s == "" or s.lower() == "nan":
        return ""

    # Repair Excel-mangled numeric formats (scientific notation, floats,
    # stray decimal points) before we start stripping characters.
    s = _repair_excel_mangled_number(s)

    # Remove everything except digits (keep only digits from here on -
    # the country-code logic below re-adds the leading +).
    digits = re.sub(r"[^\d]", "", s)

    if digits == "":
        return ""

    # Normalize prefixes step by step
    # Case: 00971XXXXXXXXX (international dialing prefix)
    if digits.startswith("00971"):
        digits = digits[2:]  # strip the leading 00 -> becomes 971XXXXXXXXX

    # Case: already has 971 country code (with or without leading +)
    elif digits.startswith("971"):
        pass  # already good

    # Case: local format starting with 0 (e.g. 0501234567)
    elif digits.startswith("0"):
        digits = "971" + digits[1:]

    # Case: no leading 0, no country code (e.g. 501234567)
    else:
        digits = "971" + digits

    # Basic sanity check: UAE mobile numbers -> 971 + 9 digits = 12 digits total
    # We still return best-effort formatting even if length looks off,
    # but flag it separately in the app.
    return "+" + digits


def is_valid_uae_number(formatted: str) -> bool:
    # Expect +971 followed by exactly 9 digits
    return bool(re.fullmatch(r"\+971\d{9}", formatted))


uploaded_file = st.file_uploader("Drop your Excel or CSV file here", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.rsplit(".", 1)[-1].lower()

    try:
        if file_ext == "csv":
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

    st.success(f"File loaded \u2014 {df.shape[0]} rows, {df.shape[1]} columns.")
    st.dataframe(df.head(10), use_container_width=True)

    # Try to auto-detect a phone-number-like column
    likely_cols = [c for c in df.columns if re.search(r"phone|mobile|number|contact|tel", str(c), re.I)]
    default_col = likely_cols[0] if likely_cols else df.columns[0]

    phone_col = st.selectbox(
        "Which column contains the phone numbers?",
        options=list(df.columns),
        index=list(df.columns).index(default_col),
    )

    new_col_name = st.text_input(
        "Name for the new formatted column",
        value=f"{phone_col}_formatted",
    )

    overwrite = st.checkbox("Overwrite the original column instead of adding a new one", value=False)

    # ------------------------------------------------------------------
    # FIX: Streamlit reruns the entire script on every widget interaction
    # (including clicking the download-format radio button or the
    # download button itself). `st.button(...)` only returns True for the
    # single rerun that happens right after it's clicked - on the very
    # next rerun it goes back to False. Since the original code put the
    # results, the radio button, and the download button all *inside*
    # `if st.button("Format phone numbers"):`, interacting with the radio
    # button caused a rerun where the button was False again, wiping out
    # the whole block - including the download button - before the file
    # could actually be downloaded.
    #
    # The fix: compute the results once and stash them in
    # st.session_state when the button is clicked, then render the
    # preview/download UI from session_state on every rerun, independent
    # of the button's transient True/False value.
    # ------------------------------------------------------------------
    if st.button("Format phone numbers", type="primary"):
        formatted = df[phone_col].apply(clean_and_format_number)
        valid_mask = formatted.apply(is_valid_uae_number)

        result_df = df.copy()
        target_col = phone_col if overwrite else new_col_name
        result_df[target_col] = formatted

        st.session_state["result_df"] = result_df
        st.session_state["valid_mask"] = valid_mask
        st.session_state["target_col"] = target_col
        st.session_state["phone_col"] = phone_col

    if "result_df" in st.session_state:
        result_df = st.session_state["result_df"]
        valid_mask = st.session_state["valid_mask"]
        target_col = st.session_state["target_col"]
        src_col = st.session_state["phone_col"]

        st.subheader("Results")
        st.write(f"\u2705 {valid_mask.sum()} numbers formatted successfully.")
        if (~valid_mask).sum() > 0:
            st.warning(
                f"\u26A0\uFE0F {(~valid_mask).sum()} numbers don't match the standard "
                f"+971 + 9-digit pattern after cleaning \u2014 please review them below "
                f"(these may have lost precision from Excel's scientific-notation export)."
            )
            st.dataframe(
                result_df.loc[~valid_mask, [src_col, target_col]],
                use_container_width=True,
            )

        st.subheader("Preview")
        st.dataframe(result_df.head(20), use_container_width=True)

        # Let the user pick the download format
        download_format = st.radio(
            "Download format",
            options=["Excel (.xlsx)", "CSV (.csv)"],
            horizontal=True,
            key="download_format",
        )

        if download_format == "CSV (.csv)":
            # CSV files carry no cell-type information. When Excel later
            # opens the CSV, it auto-detects a value like "+971501234567"
            # as a number (the leading "+" reads as a numeric sign to
            # Excel) and, because it's a 12-13 digit number, re-applies
            # its default "General" number format - which switches long
            # numbers to scientific/decimal notation. That reintroduces
            # exactly the problem this app fixes, just on the way back
            # into Excel.
            #
            # The standard workaround is to force the phone-number column
            # to be read as literal text by wrapping each value as an
            # Excel "text-literal" formula: ="+971501234567". Excel then
            # displays the value exactly as written, with no numeric
            # reinterpretation, no decimals, and no scientific notation.
            # (The .xlsx download doesn't need this - openpyxl already
            # writes the value as a real string cell type.)
            csv_export_df = result_df.copy()
            csv_export_df[target_col] = csv_export_df[target_col].apply(
                lambda v: f'="{v}"' if v else v
            )
            csv_bytes = csv_export_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="\u2B07\uFE0F Download formatted CSV file",
                data=csv_bytes,
                file_name="phone_numbers_formatted.csv",
                mime="text/csv",
            )
        else:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False, sheet_name="Sheet1")
            output.seek(0)

            st.download_button(
                label="\u2B07\uFE0F Download formatted Excel file",
                data=output,
                file_name="phone_numbers_formatted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
else:
    # Clear stale results if a new/no file is present, so old data
    # doesn't linger in session_state across uploads.
    for key in ("result_df", "valid_mask", "target_col", "phone_col"):
        st.session_state.pop(key, None)
    st.info("Waiting for a file to be uploaded...")
