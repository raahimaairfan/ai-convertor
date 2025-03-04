import os
import spacy
import re

import streamlit as st

# Install dependencies at runtime (to ensure correct versions)
os.system("pip install --no-cache-dir spacy numpy cython")

# Download spaCy model if missing
os.system("python -m spacy download en_core_web_sm")

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])  # Disable ML features

def extract_conversion_details(text):
    """Extracts number, source unit, and target unit from user input."""
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text.lower().strip())
    doc = nlp(text)
    num, from_unit, to_unit = None, None, None
    
    tokens = [token.text for token in doc]
    for i, token in enumerate(tokens):
        if token.replace('.', '', 1).isdigit():
            num = float(token)
        elif token in unit_aliases:
            if from_unit is None:
                from_unit = unit_aliases[token]
            else:
                to_unit = unit_aliases[token]
    return num, from_unit, to_unit

# Unit conversion dictionary
unit_aliases = {
    "m": "meter", "meter": "meter", "meters": "meter",
    "km": "kilometer", "kilometer": "kilometer", "kilometers": "kilometer",
    "mile": "mile", "miles": "mile",
    "yard": "yard", "yards": "yard",
    "foot": "foot", "feet": "foot",
    "g": "gram", "gram": "gram", "grams": "gram",
    "kg": "kilogram", "kilogram": "kilogram", "kilograms": "kilogram",
    "lb": "pound", "pound": "pound", "pounds": "pound",
    "oz": "ounce", "ounce": "ounce", "ounces": "ounce",
    "c": "celsius", "celsius": "celsius",
    "f": "fahrenheit", "fahrenheit": "fahrenheit",
    "k": "kelvin", "kelvin": "kelvin"
}

# Conversion functions
def length_converter(value, from_unit, to_unit):
    factors = {"meter": 1, "kilometer": 0.001, "mile": 0.000621371, "yard": 1.09361, "foot": 3.28084}
    return value * (factors[to_unit] / factors[from_unit])

def weight_converter(value, from_unit, to_unit):
    factors = {"gram": 1, "kilogram": 0.001, "pound": 0.00220462, "ounce": 0.035274}
    return value * (factors[to_unit] / factors[from_unit])

def temperature_converter(value, from_unit, to_unit):
    conversions = {
        ("celsius", "fahrenheit"): (value * 9/5) + 32,
        ("fahrenheit", "celsius"): (value - 32) * 5/9,
        ("celsius", "kelvin"): value + 273.15,
        ("kelvin", "celsius"): value - 273.15,
        ("fahrenheit", "kelvin"): (value - 32) * 5/9 + 273.15,
        ("kelvin", "fahrenheit"): (value - 273.15) * 9/5 + 32
    }
    return conversions.get((from_unit, to_unit), value)

def main():
    # Sidebar Documentation
    with st.sidebar:
        st.title("📘 Documentation")
        st.markdown("""
        ## Overview  
        Convert units easily with **Manual Mode** or **AI Mode**.  
        
        ## How to Use  
        1. **Select Mode**: Choose between Manual or AI Mode.  
        2. **Manual Mode**: Pick units from dropdowns and enter a value.  
        3. **AI Mode**: Type naturally, like "Convert 5 kg to pounds".  
        4. **Get Result**: Instant conversion!  
        
        ## Supported Units  
        - Length, Mass, Temperature, Speed, Time, Volume, and more!  
        """)
        
        st.markdown("""
        ## Common Mistakes (Avoid These!)  
        ❌ **Missing numbers**: "Convert kg to pounds" (❌ No quantity mentioned)  
        ✅ Correct: "Convert **5 kg** to pounds"  
        
        ❌ **Unclear unit names**: "Convert 10 gm to lbs" (❌ "gm" and "lbs" not recognized)  
        ✅ Correct: "Convert **10 grams** to pounds"  
        
        ❌ **Confusing phrasing**: "10 to meters from yards" (❌ Wrong word order)  
        ✅ Correct: "Convert **10 yards** to meters"  
        """)
    
    st.title("🌟 AI-Powered Unit Converter")
    mode = st.radio("Choose Conversion Mode:", ["Manual (Dropdowns)", "AI Mode (Free-text)"], index=1)
    
    if mode == "Manual (Dropdowns)":
        st.subheader("Manual Conversion")
        category = st.selectbox("Select Category", ["Length", "Weight", "Temperature"])
        unit_options = {
            "Length": ["meter", "kilometer", "mile", "yard", "foot"],
            "Weight": ["gram", "kilogram", "pound", "ounce"],
            "Temperature": ["celsius", "fahrenheit", "kelvin"]
        }
        from_unit = st.selectbox("From:", unit_options[category])
        to_unit = st.selectbox("To:", unit_options[category])
        value = st.number_input("Enter Value:", min_value=0.0, step=0.1)
        
        if st.button("Convert"):
            result = (length_converter(value, from_unit, to_unit) if category == "Length" else
                      weight_converter(value, from_unit, to_unit) if category == "Weight" else
                      temperature_converter(value, from_unit, to_unit))
            st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
    
    else:
        st.subheader("AI-Powered Conversion")
        user_input = st.text_input("Enter your conversion request (e.g., 'Convert 10 km to miles'):")
        
        if st.button("Ask AI"):
            num, from_unit, to_unit = extract_conversion_details(user_input)
            if num is None or from_unit is None or to_unit is None:
                st.error("⚠️ Could not understand your input. Try 'Convert 5 kg to pounds'.")
            else:
                converter = (length_converter if from_unit in ["meter", "kilometer", "mile", "yard", "foot"] else
                             weight_converter if from_unit in ["gram", "kilogram", "pound", "ounce"] else
                             temperature_converter)
                result = converter(num, from_unit, to_unit)
                st.success(f"✅ {num} {from_unit} = {result:.4f} {to_unit}")

if __name__ == "__main__":
    main()
