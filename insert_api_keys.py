def insert_api_keys():

def run_pipeline(fred_api_key, noaa_api_token):
    import sys
    sys.path.append('./code')
    import build_analysis_panel

    # Patch API keys into build_analysis_panel
    build_analysis_panel.FRED_API_KEY = fred_api_key
    build_analysis_panel.NOAA_API_TOKEN = noaa_api_token

    # Run the pipeline
    build_analysis_panel.fetch_fred_series('APU000072511')  # Example call to ensure keys are set
    # Re-run the full script logic
    exec(open('./code/build_analysis_panel.py').read(), {
        'FRED_API_KEY': fred_api_key,
        'NOAA_API_TOKEN': noaa_api_token
    })

def insert_api_keys():
    fred_api_key = input("Enter your FRED API Key: ")
    noaa_api_token = input("Enter your NOAA API Token: ")
    print("API keys loaded.")
    run_pipeline(fred_api_key, noaa_api_token)

if __name__ == '__main__':
    insert_api_keys()
