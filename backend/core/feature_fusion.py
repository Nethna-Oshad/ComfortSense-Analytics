import pandas as pd

def process_live_telemetry(payload_data: list, session_start_time: str):
    """
    Fuses incoming MQTT telemetry into a normalized feature vector.
    payload_data: List of dictionaries representing recent sensor readings.
    """
    df = pd.DataFrame(payload_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort chronologically
    df = df.sort_values(by='timestamp')
    
    # Calculate Air Stagnation Rate (ASR)
    df['ASR'] = df['CO2'].diff() / 5.0
    df['ASR'] = df['ASR'].fillna(0) # Handle the first reading
    
    # Calculate Elapsed Time in minutes
    start_time = pd.to_datetime(session_start_time)
    df['elapsed_time_min'] = (df['timestamp'] - start_time).dt.total_seconds() / 60.0
    
    # Select the latest reading for the prediction
    latest_reading = df.iloc[-1:]
    
    # Order features exactly as the model expects them
    features = ['temperature', 'humidity', 'noise', 'CO2', 'ASR', 'elapsed_time_min', 'peopleCount']
    return latest_reading[features]