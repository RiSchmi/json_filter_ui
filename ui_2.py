import streamlit as st
import json
# Example JSON (analysis) - replace with your actual data or import from a file
with open('analysis.json', 'r') as file:
    analysis = json.load(file)

# ----------------------------------------------------
# HELPER: Filter function
# ----------------------------------------------------
def filter_analysis(data, selected_dimensions, filter_positive, filter_negative, selected_methods):
    """
    data                -> The JSON dictionary (analysis)
    selected_dimensions -> List of dimension strings chosen by the user
                          e.g. ["Economy", "Environment"] ...
    filter_positive     -> Boolean or None; if True, dimension must have Positive_impact == True
    filter_negative     -> Boolean or None; if True, dimension must have Negative_impact == True
    selected_methods    -> List of method categories chosen by the user
    """
    filtered_results = {}

    for key, record in data.items():
        keep_record = False

        # If no dimensions selected, we ignore dimension filtering for 'Relevant'
        if not selected_dimensions:
            keep_record = True
        else:
            for dim in selected_dimensions:
                dim_data = record.get(dim, {})

                # Must be relevant if user selected it
                if dim_data.get("Relevant") is True:
                    # Check positive/negative filter if set
                    if filter_positive is not None:
                        if dim_data.get("Positive_impact") != filter_positive:
                            continue
                    if filter_negative is not None:
                        if dim_data.get("Negative_impact") != filter_negative:
                            continue

                    # Check method categories if user selected any
                    if selected_methods:
                        method_str = dim_data.get("Method Type", "")
                        # We keep the record if any selected method category
                        # text is found in method_str (case-insensitive check)
                        if not any(mcat.lower() in method_str.lower() for mcat in selected_methods):
                            continue
                    # Passed all checks for this dimension
                    keep_record = True
                    break

        if keep_record:
            filtered_results[key] = record

    return filtered_results

# ----------------------------------------------------
# STREAMLIT APP
# ----------------------------------------------------
def main():
    st.title("Digitalization/ Digital Economy Impact Filter")

    # ---------------------------
    # 1. Dimensions
    # ---------------------------
    st.markdown("### 1. Select Dimensions: Economy / Environment / Social / Security")
    dimension_options = ["Economy", "Environment", "Social", "Security"]
    selected_dimensions = st.multiselect(
        "Choose dimension(s) - OR not AND (leave empty for all) ",
        dimension_options
        
    )

    # ---------------------------
    # 2. Positive / Negative Impact
    # ---------------------------
    st.markdown("### 2. Filter by Positive / Negative Impact (Optional)")
    filter_positive = st.checkbox("Only show records with a Positive Impact", value=False)
    filter_negative = st.checkbox("Only show records with a Negative Impact", value=False)

    # If the checkbox is checked, interpret that as True. If not, None (i.e., ignore).
    filter_positive_val = True if filter_positive else None
    filter_negative_val = True if filter_negative else None

    # ---------------------------
    # 3. Method Type
    # ---------------------------
    st.markdown("### 3. Filter by Method Type (Optional)")
    method_categories = [
        "Quantitative Analysis Methods",
        "Qualitative Research Methods",
        "Systematic Reviews and Literature Analyses",
        "Cost-Benefit and Economic Assessments",
        "Mixed-Methods Approaches",
        "Modeling and Simulation Techniques"
    ]
    selected_methods = st.multiselect(
        "Select one or more method categories to match in the record's 'Method' field",
        method_categories
    )

    st.markdown("---")
    st.markdown("### Filtered Results")

    # Perform filtering
    filtered_results = filter_analysis(
        analysis,
        selected_dimensions,
        filter_positive_val,
        filter_negative_val,
        selected_methods
    )

    # Number of matched records
    st.write(f"**Number of matched records:** {len(filtered_results)}")

    # ---------------------------
    # Display filtered results
    # ---------------------------
    for key, record in filtered_results.items():
        st.markdown(f"#### {record.get('Name_publication', 'N/A')}")
        st.write(f"**File Name:** {record.get('file_name', 'N/A')}")
        st.write(f"**Name of publication:** {record.get('Name_publication', 'N/A')}")
        st.write(f"**Year:** {record.get('Year', 'N/A')}")

        # Decide which dimensions to show:
        # - If user selected none, show all relevant dimensions
        # - If user selected some, show only those
        if selected_dimensions:
            dims_to_show = selected_dimensions
        else:
            dims_to_show = dimension_options  # i.e., all possible

        for dim in dims_to_show:
            dim_data = record.get(dim, {})
            # Only show if relevant == True
            if dim_data.get("Relevant") is True:
                st.markdown(f"**{dim}**")
                st.write(f"- **Impact:** {dim_data.get('Impact', 'N/A')}")
                st.write(f"- **Positive Impact:** {dim_data.get('Positive_impact', 'N/A')}")
                st.write(f"- **Negative Impact:** {dim_data.get('Negative_impact', 'N/A')}")
                st.write(f"- **Mechanism:** {dim_data.get('Mechanism', 'N/A')}")
                st.write(f"- **Method:** {dim_data.get('Method', 'N/A')}")
                st.write(f"- **Method Type:** {dim_data.get('Method Type', 'N/A')}")
                st.write(f"- **(Data) Source:** {dim_data.get('Source', 'N/A')}")

                # Show quotes if present
                quotes = dim_data.get("Quotes")
                if isinstance(quotes, list) and quotes:
                    st.write("**Quotes:**")
                    for q in quotes:
                        st.markdown(f"> {q}")

        st.markdown("---")


if __name__ == "__main__":
    main()
