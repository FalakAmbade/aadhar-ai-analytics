import os
import sys
from dotenv import load_dotenv

# Pehle env load karna 
load_dotenv()

# Imports from src folder
from src.loader import load_csv
from src.analyzer import (
    age_wise_coverage, youth_pressure, adult_saturation, 
    temporal_growth, district_disparity, pincode_coverage, 
    youth_adult_ratio, state_concentration, longitudinal_stability,
    resource_allocation, adult_enrollment_mapping
)
from src.visualizer import generate_graph
from src.prompt_router import route_prompt

def main():
    print("--- Aadhaar AI Analytics System ---")
    
    # -----------------------------
    # 1. Debugging API Key
    # -----------------------------
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Testing API Key Status: {'Loaded' if api_key else 'NOT FOUND (Check .env file)'}")
    
    if not api_key:
        print("Error: .env file mein GEMINI_API_KEY nahi mili. Program exit ho raha hai.")
        return

    # -----------------------------
    # 2. Path Configuration
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Ensure file name matches exactly with your folder
    csv_path = os.path.join(BASE_DIR, "data", "input", "aadhar_clean.csv")

    # Topic to Function Mapping
    ANALYSIS_MAP = {
        "Age-wise Aadhaar Coverage Imbalance": age_wise_coverage,
        "Regional Youth Population Pressure": youth_pressure,
        "Adult Enrollment Saturation Mapping": adult_enrollment_mapping,
        "Temporal Growth Pattern Analysis": temporal_growth,
        "District-Level Demographic Disparity": district_disparity,
        "Pincode-Level Coverage Gaps": pincode_coverage,
        "Youth-to-Adult Ratio Risk Zones": youth_adult_ratio,
        "State-wise Demographic Concentration": state_concentration,
        "Longitudinal Stability Assessment": longitudinal_stability,
        "Resource Allocation Optimization": resource_allocation
    }

    # -----------------------------
    # 3. Data Loading
    # -----------------------------
    if not os.path.exists(csv_path):
        print(f"Error: Data file nahi mili at: {csv_path}")
        return

    print("Loading CSV file... (Big files may take a moment)")
    df = load_csv(csv_path, use_chunks=True)
    
    if df is None or df.empty:
        print("Error: DataFrame load nahi ho paya ya empty hai.")
        return
        
    print(f"Data Loaded! Total rows: {len(df)}")

    # -----------------------------
    # 4. User Interaction
    # -----------------------------
    user_prompt = input("\nAapka Aadhaar query kya hai? ")

    print("\nGemini AI routing process mein hai...")
    problem_labels = route_prompt(user_prompt)

    if not problem_labels:
        print("Gemini ne koi matching topic return nahi kiya. Query check karein.")
        return

    print(f"Mapped Topics: {problem_labels}")
    # 5. Execution & Visualization
    for problem in problem_labels:
        if problem in ANALYSIS_MAP:
            print(f"\nProcessing: {problem}...")
            try:
                # Call analyzer function
                result_df = ANALYSIS_MAP[problem](df)
                
                if result_df is not None and not result_df.empty:
                    # Smart graph selection
                    g_type = "line" if "Temporal" in problem or "Longitudinal" in problem else "bar"
                    generate_graph(result_df, graph_type=g_type, title=problem)
                else:
                    print(f"Result empty for: {problem}")
            except Exception as e:
                print(f"Error executing {problem}: {e}")
        else:
            print(f"Warning: '{problem}' mapping mein nahi mila.")

    print("\n--- Process Complete. Check data/output/graphs/ ---")

if __name__ == "__main__":
    main()
