import pandas as pd
import numpy as np
import datetime
from scipy.ndimage import gaussian_filter1d

# --- Configuration ---
NUM_HOURS = 24 # Simulating a 24-hour race
SAMPLE_RATE_SECONDS = 1
TOTAL_SAMPLES = NUM_HOURS * 3600 // SAMPLE_RATE_SECONDS
OUTPUT_FILENAME = "consistent_race_data.csv"

# --- Realistic Parameter Ranges & Initial Values ---

# Car State (initial values and typical operating ranges/changes)
CAR_PARAMS = {
    'tire_temp_FL': {'init': 90, 'std_dev': 1.5, 'stress_factor': 1.05},
    'tire_temp_FR': {'init': 90, 'std_dev': 1.5, 'stress_factor': 1.05},
    'tire_temp_RL': {'init': 90, 'std_dev': 1.5, 'stress_factor': 1.05},
    'tire_temp_RR': {'init': 90, 'std_dev': 1.5, 'stress_factor': 1.05},
    'tire_pressure_FL': {'init': 30.0, 'std_dev': 0.1, 'brake_effect': -0.1},
    'tire_pressure_FR': {'init': 30.0, 'std_dev': 0.1, 'brake_effect': -0.1},
    'tire_pressure_RL': {'init': 30.0, 'std_dev': 0.1, 'brake_effect': -0.1},
    'tire_pressure_RR': {'init': 30.0, 'std_dev': 0.1, 'brake_effect': -0.1},
    'tire_wear_rate': {'init': 0.0, 'increase_per_hour': 0.04, 'max': 1.0}, # Max wear over 24h
    'brake_disc_temp_FL': {'init': 350, 'std_dev': 10, 'spike_max': 700, 'decay_rate': 0.95},
    'brake_disc_temp_FR': {'init': 350, 'std_dev': 10, 'spike_max': 700, 'decay_rate': 0.95},
    'brake_disc_temp_RL': {'init': 350, 'std_dev': 10, 'spike_max': 650, 'decay_rate': 0.95},
    'brake_disc_temp_RR': {'init': 350, 'std_dev': 10, 'spike_max': 650, 'decay_rate': 0.95},
    'brake_pedal_pressure': {'init': 0, 'std_dev': 5, 'max': 100},
    'engine_rpm': {'init': 7000, 'std_dev': 100},
    'coolant_temperature': {'init': 95, 'std_dev': 0.2, 'stress_increase': 0.5},
    'coolant_pressure': {'init': 1.3, 'std_dev': 0.01, 'temp_effect': 0.01},
    'oil_temperature': {'init': 100, 'std_dev': 0.3, 'stress_increase': 0.7},
    'oil_pressure': {'init': 60, 'std_dev': 1, 'rpm_effect': 0.005, 'level_effect': -0.05},
    'oil_level': {'init': 1.0, 'decrease_per_hour': 0.002, 'min': 0.8}, # Simulating very slow consumption
}

# Driver Health
DRIVER_PARAMS = {
    'heart_rate': {'init': 130, 'std_dev': 1, 'fatigue_increase': 0.2, 'stress_spike': 10},
    'gsr': {'init': 4, 'std_dev': 0.1, 'fatigue_increase': 0.05, 'stress_spike': 2},
    'pupil_dilation': {'init': 4.5, 'std_dev': 0.05, 'fatigue_increase': 0.01},
    'blink_rate': {'init': 18, 'std_dev': 0.1, 'fatigue_decrease': 0.1},
}

# Environmental Condition
ENV_PARAMS = {
    'rainfall_intensity': {'init': 0.0, 'max_rain': 10.0, 'rain_duration_hours': 2, 'start_hour': 5},
    'track_temperature': {'init': 35, 'std_dev': 0.5, 'rain_effect': -5, 'night_effect': -0.2},
    'ambient_light': {'init': 70000, 'std_dev': 1000, 'night_start_hour': 18, 'night_end_hour': 6},
}

# Smoothing factor for sensor readings (higher = smoother)
SMOOTHING_SIGMA = 20 # Applied after initial generation to mimic sensor inertia

# --- Data Generation Logic ---

def generate_race_data():
    data = {}
    current_values = {
        **{k: v['init'] for k, v in CAR_PARAMS.items()},
        **{k: v['init'] for k, v in DRIVER_PARAMS.items()},
        **{k: v['init'] for k, v in ENV_PARAMS.items()}
    }
    
    # Initialize lists to store time series data
    timestamps = []
    for k in CAR_PARAMS: data[k] = []
    for k in DRIVER_PARAMS: data[k] = []
    for k in ENV_PARAMS: data[k] = []

    start_time = datetime.datetime.now()
    
    # Simulate specific events
    braking_events = np.random.choice(TOTAL_SAMPLES, TOTAL_SAMPLES // 100, replace=False) # ~1% of samples are braking events
    hard_acceleration_events = np.random.choice(TOTAL_SAMPLES, TOTAL_SAMPLES // 200, replace=False) # ~0.5% are hard accel
    
    rain_started = False
    
    print(f"Generating {TOTAL_SAMPLES} data points over {NUM_HOURS} hours...")

    for i in range(TOTAL_SAMPLES):
        timestamp = start_time + datetime.timedelta(seconds=i * SAMPLE_RATE_SECONDS)
        timestamps.append(timestamp)

        # Calculate time in hours for environmental and fatigue trends
        time_in_hours = i * SAMPLE_RATE_SECONDS / 3600

        # --- Environmental Data Simulation (smooth transitions) ---
        # Ambient Light (Day/Night cycle)
        if time_in_hours >= ENV_PARAMS['ambient_light']['night_start_hour'] or time_in_hours < ENV_PARAMS['ambient_light']['night_end_hour']:
            # Night time, very low light
            current_values['ambient_light'] = np.interp(time_in_hours % 24, [ENV_PARAMS['ambient_light']['night_start_hour'], ENV_PARAMS['ambient_light']['night_end_hour'] + 24], [1000, 100]) # Example 18:00 to 06:00
            current_values['ambient_light'] = max(50, current_values['ambient_light'] + np.random.normal(0, ENV_PARAMS['ambient_light']['std_dev'] / 10))
        else:
            # Daytime, high light
            current_values['ambient_light'] = np.interp(time_in_hours % 24, [ENV_PARAMS['ambient_light']['night_end_hour'], ENV_PARAMS['ambient_light']['night_start_hour']], [30000, 80000]) # Example 06:00 to 18:00
            current_values['ambient_light'] = max(10000, current_values['ambient_light'] + np.random.normal(0, ENV_PARAMS['ambient_light']['std_dev']))
        
        # Rainfall Intensity
        if ENV_PARAMS['rainfall_intensity']['start_hour'] <= time_in_hours < ENV_PARAMS['rainfall_intensity']['start_hour'] + ENV_PARAMS['rainfall_intensity']['rain_duration_hours']:
            if not rain_started:
                # Smooth transition into rain
                current_values['rainfall_intensity'] = np.interp((time_in_hours - ENV_PARAMS['rainfall_intensity']['start_hour']) / ENV_PARAMS['rainfall_intensity']['rain_duration_hours'], [0, 0.1], [0, ENV_PARAMS['rainfall_intensity']['max_rain'] / 2])
                rain_started = True
            else:
                current_values['rainfall_intensity'] = np.random.uniform(ENV_PARAMS['rainfall_intensity']['max_rain'] * 0.7, ENV_PARAMS['rainfall_intensity']['max_rain']) + np.random.normal(0, 0.5)
        elif rain_started:
            # Smooth transition out of rain
            current_values['rainfall_intensity'] = max(0.0, current_values['rainfall_intensity'] * 0.95 + np.random.normal(0, 0.1)) # Gradual decay
            if current_values['rainfall_intensity'] < 0.1: rain_started = False
        else:
            current_values['rainfall_intensity'] = 0.0

        # Track Temperature (influenced by ambient light and rain)
        temp_base = ENV_PARAMS['track_temperature']['init'] + np.random.normal(0, ENV_PARAMS['track_temperature']['std_dev'])
        if current_values['rainfall_intensity'] > 0:
            temp_base += ENV_PARAMS['track_temperature']['rain_effect']
        if current_values['ambient_light'] < 1000: # Night
            temp_base += ENV_PARAMS['track_temperature']['night_effect'] * (time_in_hours % 24 - ENV_PARAMS['ambient_light']['night_start_hour'])
        current_values['track_temperature'] = temp_base


        # --- Car State Simulation ---
        # Engine RPM (simulate variations)
        if i in hard_acceleration_events:
            current_values['engine_rpm'] = 9500 # Short burst
        else:
            current_values['engine_rpm'] = current_values['engine_rpm'] * 0.95 + 0.05 * CAR_PARAMS['engine_rpm']['init'] + np.random.normal(0, CAR_PARAMS['engine_rpm']['std_dev'])
            current_values['engine_rpm'] = np.clip(current_values['engine_rpm'], 5000, 9000) # Keep within typical race RPM

        # Brake Pedal Pressure & Brake Disc Temp (Event-driven)
        brake_pressure_current = 0
        brake_temp_spike = 0
        if i in braking_events:
            brake_pressure_current = CAR_PARAMS['brake_pedal_pressure']['max'] * np.random.uniform(0.6, 1.0)
            brake_temp_spike = np.random.uniform(1.2, 1.5) # Factor to increase temp
        else:
            # Gradual decay of pressure
            brake_pressure_current = current_values['brake_pedal_pressure'] * 0.85 + np.random.normal(0, CAR_PARAMS['brake_pedal_pressure']['std_dev'])
            brake_pressure_current = max(0, brake_pressure_current)

        current_values['brake_pedal_pressure'] = brake_pressure_current
        
        for side in ['FL', 'FR', 'RL', 'RR']:
            temp_key = f'brake_disc_temp_{side}'
            
            # Decay from previous temp, add base, then spike if braking
            current_values[temp_key] = current_values[temp_key] * CAR_PARAMS[temp_key]['decay_rate'] + (CAR_PARAMS[temp_key]['init'] * (1 - CAR_PARAMS[temp_key]['decay_rate']))
            current_values[temp_key] += np.random.normal(0, CAR_PARAMS[temp_key]['std_dev'])
            
            if brake_temp_spike > 0:
                current_values[temp_key] = min(CAR_PARAMS[temp_key]['spike_max'], current_values[temp_key] * brake_temp_spike)
            current_values[temp_key] = max(CAR_PARAMS[temp_key]['init'] * 0.8, current_values[temp_key]) # Prevent going too low

        # Tire Temps and Pressures (influenced by RPM, braking, track temp)
        for side in ['FL', 'FR', 'RL', 'RR']:
            temp_key = f'tire_temp_{side}'
            pressure_key = f'tire_pressure_{side}'
            
            # Temp influenced by RPM, brake temp, and track temp
            temp_change = (current_values['engine_rpm'] / 9000) * 0.5 + (current_values[f'brake_disc_temp_{side}'] / 700) * 0.8
            current_values[temp_key] = current_values[temp_key] * 0.98 + (CAR_PARAMS[temp_key]['init'] * 0.02) + temp_change + np.random.normal(0, CAR_PARAMS[temp_key]['std_dev'])
            current_values[temp_key] = np.clip(current_values[temp_key], 70, 120)

            # Pressure influenced by temp, and small random walk
            pressure_change = (current_values[temp_key] - CAR_PARAMS[temp_key]['init']) * 0.01 # Temp effect on pressure
            current_values[pressure_key] = current_values[pressure_key] + pressure_change + np.random.normal(0, CAR_PARAMS[pressure_key]['std_dev'])
            current_values[pressure_key] = np.clip(current_values[pressure_key], 28, 32)
            
        # Tire Wear Rate (gradual increase over time)
        current_values['tire_wear_rate'] = min(CAR_PARAMS['tire_wear_rate']['max'], current_values['tire_wear_rate'] + (CAR_PARAMS['tire_wear_rate']['increase_per_hour'] / 3600) * SAMPLE_RATE_SECONDS + np.random.normal(0, 0.00001))

        # Coolant and Oil Temperatures (influenced by RPM)
        current_values['coolant_temperature'] = current_values['coolant_temperature'] * 0.99 + CAR_PARAMS['coolant_temperature']['init'] * 0.01 + (current_values['engine_rpm'] / 9000) * CAR_PARAMS['coolant_temperature']['stress_increase'] + np.random.normal(0, CAR_PARAMS['coolant_temperature']['std_dev'])
        current_values['coolant_temperature'] = np.clip(current_values['coolant_temperature'], 85, 110)
        
        current_values['coolant_pressure'] = current_values['coolant_pressure'] * 0.99 + CAR_PARAMS['coolant_pressure']['init'] * 0.01 + (current_values['coolant_temperature'] - 95) * CAR_PARAMS['coolant_pressure']['temp_effect'] + np.random.normal(0, CAR_PARAMS['coolant_pressure']['std_dev'])
        current_values['coolant_pressure'] = np.clip(current_values['coolant_pressure'], 1.0, 1.8)

        current_values['oil_temperature'] = current_values['oil_temperature'] * 0.99 + CAR_PARAMS['oil_temperature']['init'] * 0.01 + (current_values['engine_rpm'] / 9000) * CAR_PARAMS['oil_temperature']['stress_increase'] + np.random.normal(0, CAR_PARAMS['oil_temperature']['std_dev'])
        current_values['oil_temperature'] = np.clip(current_values['oil_temperature'], 90, 120)
        
        current_values['oil_pressure'] = current_values['oil_pressure'] * 0.98 + CAR_PARAMS['oil_pressure']['init'] * 0.02 + (current_values['engine_rpm'] / 9000) * CAR_PARAMS['oil_pressure']['rpm_effect'] * 100 + (1 - current_values['oil_level']) * CAR_PARAMS['oil_pressure']['level_effect'] * 100 + np.random.normal(0, CAR_PARAMS['oil_pressure']['std_dev'])
        current_values['oil_pressure'] = np.clip(current_values['oil_pressure'], 40, 80)

        # Oil Level (gradual decrease over time)
        current_values['oil_level'] = max(CAR_PARAMS['oil_level']['min'], current_values['oil_level'] - (CAR_PARAMS['oil_level']['decrease_per_hour'] / 3600) * SAMPLE_RATE_SECONDS + np.random.normal(0, 0.000001))

        # --- Driver Health Simulation (fatigue builds over time) ---
        fatigue_level = min(1.0, time_in_hours / NUM_HOURS * 2) # Fatigue increases non-linearly
        
        # Heart Rate (influenced by fatigue and car stress - e.g., hard braking events)
        hr_change = (current_values['engine_rpm'] / 9000) * DRIVER_PARAMS['heart_rate']['stress_spike'] * 0.5
        if i in braking_events or i in hard_acceleration_events:
            hr_change += DRIVER_PARAMS['heart_rate']['stress_spike'] * np.random.uniform(0.5, 1.0) # Spike
        current_values['heart_rate'] = current_values['heart_rate'] * 0.95 + DRIVER_PARAMS['heart_rate']['init'] * 0.05 + fatigue_level * DRIVER_PARAMS['heart_rate']['fatigue_increase'] + hr_change + np.random.normal(0, DRIVER_PARAMS['heart_rate']['std_dev'])
        current_values['heart_rate'] = np.clip(current_values['heart_rate'], 100, 180)

        # GSR (influenced by fatigue and car stress)
        gsr_change = (current_values['engine_rpm'] / 9000) * DRIVER_PARAMS['gsr']['stress_spike'] * 0.2
        if i in braking_events or i in hard_acceleration_events:
            gsr_change += DRIVER_PARAMS['gsr']['stress_spike'] * np.random.uniform(0.5, 1.0) # Spike
        current_values['gsr'] = current_values['gsr'] * 0.95 + DRIVER_PARAMS['gsr']['init'] * 0.05 + fatigue_level * DRIVER_PARAMS['gsr']['fatigue_increase'] + gsr_change + np.random.normal(0, DRIVER_PARAMS['gsr']['std_dev'])
        current_values['gsr'] = np.clip(current_values['gsr'], 0, 15)

        # Pupil Dilation (subtle change with fatigue, also affected by light)
        light_effect_pd = np.interp(current_values['ambient_light'], [50, 80000], [6.5, 3.5]) # Inverse relationship with light
        current_values['pupil_dilation'] = current_values['pupil_dilation'] * 0.95 + light_effect_pd * 0.05 + fatigue_level * DRIVER_PARAMS['pupil_dilation']['fatigue_increase'] + np.random.normal(0, DRIVER_PARAMS['pupil_dilation']['std_dev'])
        current_values['pupil_dilation'] = np.clip(current_values['pupil_dilation'], 3.0, 7.0)

        # Blink Rate (decreases with fatigue)
        current_values['blink_rate'] = current_values['blink_rate'] * 0.95 + DRIVER_PARAMS['blink_rate']['init'] * 0.05 - fatigue_level * DRIVER_PARAMS['blink_rate']['fatigue_decrease'] + np.random.normal(0, DRIVER_PARAMS['blink_rate']['std_dev'])
        current_values['blink_rate'] = np.clip(current_values['blink_rate'], 5, 25) # Min/Max for blink rate

        # Append current values to lists
        for k in CAR_PARAMS: data[k].append(current_values[k])
        for k in DRIVER_PARAMS: data[k].append(current_values[k])
        for k in ENV_PARAMS: data[k].append(current_values[k])

    df = pd.DataFrame({'timestamp': timestamps, **data})

    # Apply Gaussian smoothing to sensor-like data for more consistency
    for col in df.columns:
        if col != 'timestamp' and col not in ['brake_pedal_pressure', 'rainfall_intensity']: # Don't smooth discrete events or rainfall
            df[col] = gaussian_filter1d(df[col], sigma=SMOOTHING_SIGMA)
    
    # Ensure some columns remain within bounds after smoothing
    df['oil_level'] = np.clip(df['oil_level'], CAR_PARAMS['oil_level']['min'], CAR_PARAMS['oil_level']['init'])
    df['tire_wear_rate'] = np.clip(df['tire_wear_rate'], 0, CAR_PARAMS['tire_wear_rate']['max'])
    df['rainfall_intensity'] = np.clip(df['rainfall_intensity'], 0, ENV_PARAMS['rainfall_intensity']['max_rain'] + 2) # Allow slight overshoot due to smoothing
    df['blink_rate'] = np.clip(df['blink_rate'], 5, 25) # Re-clip blink rate

    return df

# --- Generate and Save Data ---
generated_df = generate_race_data()
generated_df.to_csv(OUTPUT_FILENAME, index=False)

print(f"\nData generation complete. Saved to '{OUTPUT_FILENAME}' with {len(generated_df)} rows.")
print