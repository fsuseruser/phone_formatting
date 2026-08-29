import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(page_title="UAE Phone Number Formatter", page_icon="📞", layout="centered")

st.title("📞 UAE Phone Number Formatter")
st.write(
    "Upload an Excel file, pick the phone number column, and this app will clean "
    "and reformat every number to the **+971XXXXXXXXX** format."
)


def clean_and_format_number(raw_value: str) -> str:
    """
    Clean a raw phone number string and reformat it to +971XXXXXXXXX.

    Handles cases like:
      050 123 4567      -> +971501234567
      0501234567         -> +971501234567
      501234567          -> +971501234567
      971501234567       -> +971501234567
      00971501234567     -> +971501234567
      +971 50 123 4567   -> +971501234567
    """
    if raw_value is None:
        return ""

    s = str(raw_value).strip()
    if s == "" or s.lower() == "nan":
        return ""

    # Remove everything except digits and a leading '+'
    has_plus = s.strip().startswith("+")
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


uploaded_file = st.file_uploader("Drop your Excel file here", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, dtype=str)
    except Exception as e:
        st.error(f"Could not read the Excel file: {e}")
        st.stop()

    st.success(f"File loaded — {df.shape[0]} rows, {df.shape[1]} columns.")
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

    if st.button("Format phone numbers", type="primary"):
        formatted = df[phone_col].apply(clean_and_format_number)
        valid_mask = formatted.apply(is_valid_uae_number)

        result_df = df.copy()
        target_col = phone_col if overwrite else new_col_name
        result_df[target_col] = formatted

        st.subheader("Results")
        st.write(f"✅ {valid_mask.sum()} numbers formatted successfully.")
        if (~valid_mask).sum() > 0:
            st.warning(
                f"⚠️ {(~valid_mask).sum()} numbers don't match the standard "
                f"+971 + 9-digit pattern after cleaning — please review them below."
            )
            st.dataframe(
                result_df.loc[~valid_mask, [phone_col, target_col]],
                use_container_width=True,
            )

        st.subheader("Preview")
        st.dataframe(result_df.head(20), use_container_width=True)

        # Prepare downloadable Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            result_df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)

        st.download_button(
            label="⬇️ Download formatted Excel file",
            data=output,
            file_name="phone_numbers_formatted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Waiting for a file to be uploaded...")
