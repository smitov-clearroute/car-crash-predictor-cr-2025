import pandas as pd
import numpy as np
import datetime
import random
import sys

# --- Global State Variables (These will be updated by the functions) ---
_current_sample_index = 0
_current_oil_level = 100.0
_current_tire_wear = 0.0
_last_car_data = {}
_last_driver_data = {}
_last_env_data = {}

# --- Realistic Parameter Ranges & Initial Values ---

# Car State
TIRE_TEMP_BASE = 90 # Celsius, normal operating point
TIRE_TEMP_NOISE_PER_STEP = 1.0 # Max random change per step
TIRE_PRESSURE_BASE = 30.0 # PSI
TIRE_PRESSURE_NOISE_PER_STEP = 0.1 # Max random change per step
TIRE_WEAR_RATE_PER_SECOND = 0.000005 # Small increase per second (0.000005 * 3600 * 24 = ~0.43 wear over 24h)

BRAKE_DISC_TEMP_BASE = 400 # Celsius
BRAKE_DISC_TEMP_NOISE_PER_STEP = 20 # Max random change per step
BRAKE_DISC_TEMP_SPIKE_INCREMENT = 200 # How much temp jumps on a hard brake
BRAKE_DISC_TEMP_DECAY_RATE = 0.95 # Factor each step

BRAKE_PEDAL_PRESSURE_DECAY_RATE = 0.8 # Factor each step
BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP = 5 # Max random change per step

ENGINE_RPM_BASE = 7000 # RPM
ENGINE_RPM_NOISE_PER_STEP = 100 # Max random change per step

COOLANT_TEMP_BASE = 95 # Celsius
COOLANT_TEMP_NOISE_PER_STEP = 0.5 # Max random change per step
COOLANT_TEMP_STRESS_INCREASE = 0.5 # Increase per 1000 RPM over base

COOLANT_PRESSURE_BASE = 1.3 # Bar
COOLANT_PRESSURE_NOISE_PER_STEP = 0.01 # Max random change per step
COOLANT_PRESSURE_TEMP_EFFECT = 0.02 # Increase per 1 deg C over base temp

OIL_TEMP_BASE = 100 # Celsius
OIL_TEMP_NOISE_PER_STEP = 0.5 # Max random change per step
OIL_TEMP_STRESS_INCREASE = 0.8 # Increase per 1000 RPM over base

OIL_PRESSURE_BASE = 60 # PSI
OIL_PRESSURE_NOISE_PER_STEP = 0.5 # Max random change per step
OIL_PRESSURE_RPM_EFFECT = 0.005 # PSI per RPM
OIL_PRESSURE_LEVEL_EFFECT = -0.1 # PSI drop per % oil level drop

OIL_LEVEL_DECREASE_PER_SECOND = 0.000002 # Percentage drop per second (0.000002 * 3600 * 24 = ~0.17 drop over 24h)


# Driver Health
HEART_RATE_BASE = 130 # BPM
HEART_RATE_NOISE_PER_STEP = 1.0 # Max random change per step
HEART_RATE_FATIGUE_INCREASE_PER_HOUR = 2 # BPM increase per hour of fatigue
HEART_RATE_STRESS_SPIKE = 10 # BPM increase on stress event

GSR_BASE = 4 # Microsiemens
GSR_NOISE_PER_STEP = 0.1 # Max random change per step
GSR_FATIGUE_INCREASE_PER_HOUR = 0.2 # Microsiemens increase per hour of fatigue
GSR_STRESS_SPIKE = 2 # Microsiemens increase on stress event

PUPIL_DILATION_BASE = 4.5 # MM
PUPIL_DILATION_NOISE_PER_STEP = 0.05 # Max random change per step
PUPIL_DILATION_FATIGUE_INCREASE_PER_HOUR = 0.01 # MM increase per hour of fatigue
PUPIL_DILATION_LIGHT_EFFECT_FACTOR = 0.00005 # MM per Lux (inverse effect)

BLINK_RATE_BASE = 18 # Blinks per minute
BLINK_RATE_NOISE_PER_STEP = 0.2 # Max random change per step
BLINK_RATE_FATIGUE_DECREASE_PER_HOUR = 0.5 # Blinks per minute decrease per hour of fatigue


# Environmental Condition
RAINFALL_INTENSITY_NOISE_PER_STEP = 0.1 # Max random change per step
RAINFALL_MAX_INTENSITY = 10.0 # Max mm/h during rain
RAINFALL_EVENT_DURATION_SECONDS = 3600 * 4 # 4 hours of rain for demonstration
RAINFALL_EVENT_START_SECOND = 3600 * 6 # Starts 6 hours into the race

TRACK_TEMP_BASE = 35 # Celsius
TRACK_TEMP_NOISE_PER_STEP = 0.1 # Max random change per step
TRACK_TEMP_RAIN_EFFECT = -5 # Deg C drop during rain
TRACK_TEMP_NIGHT_EFFECT_PER_HOUR = -0.5 # Deg C drop per hour at night

AMBIENT_LIGHT_BASE = 70000 # Lux (daytime)
AMBIENT_LIGHT_NOISE_PER_STEP = 500 # Max random change per step
AMBIENT_LIGHT_NIGHT_THRESHOLD = 500 # Lux threshold for "night"
AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS = 3600 * 2 # 2 hours for sunset/sunrise
AMBIENT_LIGHT_NIGHT_START_HOUR = 18 # Starts to get dark at 18:00
AMBIENT_LIGHT_DAY_START_HOUR = 6 # Starts to get light at 06:00

# Event probabilities per second
BRAKING_EVENT_PROB = 0.005 # 0.5% chance per second
ACCELERATION_EVENT_PROB = 0.002 # 0.2% chance per second

def _apply_change(current_value, base_value, noise_range, trend_value=0, event_effect=0):
    """Applies a small random walk, a trend, and an event effect to a value."""
    new_value = current_value * 0.9 + base_value * 0.1 # Gravitate towards base
    new_value += np.random.uniform(-noise_range, noise_range)
    new_value += trend_value
    new_value += event_effect
    return new_value

def initialize_race_data_stream():
    """Initializes the global state for the data stream."""
    global _current_sample_index, _current_oil_level, _current_tire_wear, \
           _last_car_data, _last_driver_data, _last_env_data

    _current_sample_index = 0
    _current_oil_level = OIL_LEVEL_DECREASE_PER_SECOND # Start slightly lower for first calc
    _current_tire_wear = TIRE_WEAR_RATE_PER_SECOND # Start slightly higher for first calc

    # Set initial "last" data points to base values
    _last_car_data = {
        'tire_temp_FL': TIRE_TEMP_BASE, 'tire_temp_FR': TIRE_TEMP_BASE, 'tire_temp_RL': TIRE_TEMP_BASE, 'tire_temp_RR': TIRE_TEMP_BASE,
        'tire_pressure_FL': TIRE_PRESSURE_BASE, 'tire_pressure_FR': TIRE_PRESSURE_BASE, 'tire_pressure_RL': TIRE_PRESSURE_BASE, 'tire_pressure_RR': TIRE_PRESSURE_BASE,
        'tire_wear_rate': 0.0, # This will be updated by the _current_tire_wear in next step
        'brake_disc_temp_FL': BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_FR': BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_RL': BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_RR': BRAKE_DISC_TEMP_BASE,
        'brake_pedal_pressure': 0.0,
        'engine_rpm': ENGINE_RPM_BASE,
        'coolant_temperature': COOLANT_TEMP_BASE,
        'coolant_pressure': COOLANT_PRESSURE_BASE,
        'oil_temperature': OIL_TEMP_BASE,
        'oil_pressure': OIL_PRESSURE_BASE,
        'oil_level': 1.0 # This will be updated by the _current_oil_level in next step
    }

    _last_driver_data = {
        'heart_rate': HEART_RATE_BASE,
        'gsr': GSR_BASE,
        'pupil_dilation': PUPIL_DILATION_BASE,
        'blink_rate': BLINK_RATE_BASE
    }

    _last_env_data = {
        'rainfall_intensity': 0.0,
        'track_temperature': TRACK_TEMP_BASE,
        'ambient_light': AMBIENT_LIGHT_BASE
    }

    print("Race data stream initialized. Ready to generate first data point.")

def generate_next_data_point():
    """
    Generates a single, new data point based on the previous state and
    updates the global state for the next call.
    Returns a dictionary of the new data point.
    """
    global _current_sample_index, _current_oil_level, _current_tire_wear, \
           _last_car_data, _last_driver_data, _last_env_data


    _current_sample_index += 1
    
    current_time_in_seconds = _current_sample_index
    current_time_in_hours = current_time_in_seconds / 3600.0

    new_car_data = {}
    new_driver_data = {}
    new_env_data = {}

    # --- Environmental Data ---
    # Ambient Light (Day/Night Cycle)
    if AMBIENT_LIGHT_NIGHT_START_HOUR <= current_time_in_hours < AMBIENT_LIGHT_DAY_START_HOUR + 24: # Handles wrap-around
        if AMBIENT_LIGHT_NIGHT_START_HOUR <= current_time_in_hours < AMBIENT_LIGHT_NIGHT_START_HOUR + AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600:
            # Sunset transition
            transition_progress = (current_time_in_hours - AMBIENT_LIGHT_NIGHT_START_HOUR) / (AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600)
            new_env_data['ambient_light'] = np.interp(transition_progress, [0, 1], [AMBIENT_LIGHT_BASE, AMBIENT_LIGHT_NIGHT_THRESHOLD])
        elif AMBIENT_LIGHT_DAY_START_HOUR <= current_time_in_hours < AMBIENT_LIGHT_DAY_START_HOUR + AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600:
            # Sunrise transition (handling for 24h cycle)
            transition_progress = (current_time_in_hours - AMBIENT_LIGHT_DAY_START_HOUR) / (AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600)
            new_env_data['ambient_light'] = np.interp(transition_progress, [0, 1], [AMBIENT_LIGHT_NIGHT_THRESHOLD, AMBIENT_LIGHT_BASE])
        elif AMBIENT_LIGHT_NIGHT_START_HOUR + AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600 <= current_time_in_hours < AMBIENT_LIGHT_DAY_START_HOUR + 24:
             # Full night
             new_env_data['ambient_light'] = AMBIENT_LIGHT_NIGHT_THRESHOLD
        else:
            # Full day
            new_env_data['ambient_light'] = AMBIENT_LIGHT_BASE
    else: # Default daytime
        new_env_data['ambient_light'] = AMBIENT_LIGHT_BASE
        
    new_env_data['ambient_light'] += np.random.uniform(-AMBIENT_LIGHT_NOISE_PER_STEP, AMBIENT_LIGHT_NOISE_PER_STEP)
    new_env_data['ambient_light'] = max(10, new_env_data['ambient_light']) # Min light

    # Rainfall Intensity
    if RAINFALL_EVENT_START_SECOND <= current_time_in_seconds < RAINFALL_EVENT_START_SECOND + RAINFALL_EVENT_DURATION_SECONDS:
        # Simulate ramp-up and then steady rain
        rain_progress = (current_time_in_seconds - RAINFALL_EVENT_START_SECOND) / RAINFALL_EVENT_DURATION_SECONDS
        if rain_progress < 0.1: # Ramp up in first 10% of event
            new_env_data['rainfall_intensity'] = np.interp(rain_progress, [0, 0.1], [0, RAINFALL_MAX_INTENSITY * 0.8])
        else:
            new_env_data['rainfall_intensity'] = np.random.uniform(RAINFALL_MAX_INTENSITY * 0.7, RAINFALL_MAX_INTENSITY)
    else:
        # Decay slowly after rain event
        new_env_data['rainfall_intensity'] = max(0.0, _last_env_data['rainfall_intensity'] * 0.99 - np.random.uniform(0, RAINFALL_INTENSITY_NOISE_PER_STEP))
    new_env_data['rainfall_intensity'] = max(0.0, new_env_data['rainfall_intensity'] + np.random.uniform(-RAINFALL_INTENSITY_NOISE_PER_STEP, RAINFALL_INTENSITY_NOISE_PER_STEP))

    # Track Temperature
    track_temp_trend = TRACK_TEMP_NIGHT_EFFECT_PER_HOUR * (current_time_in_hours - 12) if 12 < current_time_in_hours < 24 else 0 # Cooler at night
    if new_env_data['rainfall_intensity'] > 0.5: # Significant rain effect
        track_temp_trend += TRACK_TEMP_RAIN_EFFECT
    new_env_data['track_temperature'] = _apply_change(_last_env_data['track_temperature'], TRACK_TEMP_BASE, TRACK_TEMP_NOISE_PER_STEP, trend_value=track_temp_trend/3600)
    new_env_data['track_temperature'] = np.clip(new_env_data['track_temperature'], 10, 50)

    # --- Car State ---
    # Engine RPM (random walk around base, occasional shifts)
    new_car_data['engine_rpm'] = _apply_change(_last_car_data['engine_rpm'], ENGINE_RPM_BASE, ENGINE_RPM_NOISE_PER_STEP)
    if random.random() < ACCELERATION_EVENT_PROB: # Hard acceleration
        new_car_data['engine_rpm'] = min(9500, new_car_data['engine_rpm'] + 1000)
    new_car_data['engine_rpm'] = np.clip(new_car_data['engine_rpm'], 5000, 9000)

    # Brake Pedal Pressure & Brake Disc Temp
    brake_event = False
    if random.random() < BRAKING_EVENT_PROB: # Simulate a braking event
        brake_event = True
        new_car_data['brake_pedal_pressure'] = np.random.uniform(50, 100)
    else:
        new_car_data['brake_pedal_pressure'] = _last_car_data['brake_pedal_pressure'] * BRAKE_PEDAL_PRESSURE_DECAY_RATE + np.random.uniform(-BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP, BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP)
        new_car_data['brake_pedal_pressure'] = max(0, new_car_data['brake_pedal_pressure']) # Can't go negative

    for side in ['FL', 'FR', 'RL', 'RR']:
        temp_key = f'brake_disc_temp_{side}'
        
        # Decay towards base, then add noise and potential spike
        new_val = _last_car_data[temp_key] * BRAKE_DISC_TEMP_DECAY_RATE + BRAKE_DISC_TEMP_BASE * (1 - BRAKE_DISC_TEMP_DECAY_RATE)
        new_val += np.random.uniform(-BRAKE_DISC_TEMP_NOISE_PER_STEP, BRAKE_DISC_TEMP_NOISE_PER_STEP)
        if brake_event:
            new_val += BRAKE_DISC_TEMP_SPIKE_INCREMENT * np.random.uniform(0.8, 1.2) # Add spike on brake event
        new_car_data[temp_key] = np.clip(new_val, BRAKE_DISC_TEMP_BASE * 0.7, BRAKE_DISC_TEMP_BASE * 1.8) # Keep within bounds

    # Tire Temps and Pressures
    for side in ['FL', 'FR', 'RL', 'RR']:
        temp_key = f'tire_temp_{side}'
        pressure_key = f'tire_pressure_{side}'
        
        # Tire Temp (influenced by engine RPM and brake temp, and track temp)
        engine_stress_factor = (new_car_data['engine_rpm'] - ENGINE_RPM_BASE) / (9000 - ENGINE_RPM_BASE) if (9000 - ENGINE_RPM_BASE) > 0 else 0
        brake_stress_factor = (new_car_data[f'brake_disc_temp_{side}'] - BRAKE_DISC_TEMP_BASE) / (BRAKE_DISC_TEMP_SPIKE_INCREMENT * 1.2) if (BRAKE_DISC_TEMP_SPIKE_INCREMENT * 1.2) > 0 else 0
        
        temp_trend = engine_stress_factor * 0.5 + brake_stress_factor * 0.5 + (new_env_data['track_temperature'] - TRACK_TEMP_BASE) * 0.1
        new_car_data[temp_key] = _apply_change(_last_car_data[temp_key], TIRE_TEMP_BASE, TIRE_TEMP_NOISE_PER_STEP, trend_value=temp_trend)
        new_car_data[temp_key] = np.clip(new_car_data[temp_key], 70, 115)

        # Tire Pressure (influenced by tire temp)
        pressure_temp_effect = (new_car_data[temp_key] - TIRE_TEMP_BASE) * 0.01
        new_car_data[pressure_key] = _apply_change(_last_car_data[pressure_key], TIRE_PRESSURE_BASE, TIRE_PRESSURE_NOISE_PER_STEP, trend_value=pressure_temp_effect)
        new_car_data[pressure_key] = np.clip(new_car_data[pressure_key], 28, 32)
        
    # Tire Wear Rate (gradually increases)
    new_car_data['tire_wear_rate'] = _current_tire_wear + TIRE_WEAR_RATE_PER_SECOND + np.random.uniform(-TIRE_WEAR_RATE_PER_SECOND/5, TIRE_WEAR_RATE_PER_SECOND/5)
    new_car_data['tire_wear_rate'] = np.clip(new_car_data['tire_wear_rate'], 0.0, 1.0) # 0-1 scale

    # Coolant Temperature
    stress_effect_ct = (new_car_data['engine_rpm'] - ENGINE_RPM_BASE) / 1000 * COOLANT_TEMP_STRESS_INCREASE
    new_car_data['coolant_temperature'] = _apply_change(_last_car_data['coolant_temperature'], COOLANT_TEMP_BASE, COOLANT_TEMP_NOISE_PER_STEP, trend_value=stress_effect_ct)
    new_car_data['coolant_temperature'] = np.clip(new_car_data['coolant_temperature'], 85, 105)

    # Coolant Pressure
    pressure_effect_cp = (new_car_data['coolant_temperature'] - COOLANT_TEMP_BASE) * COOLANT_PRESSURE_TEMP_EFFECT
    new_car_data['coolant_pressure'] = _apply_change(_last_car_data['coolant_pressure'], COOLANT_PRESSURE_BASE, COOLANT_PRESSURE_NOISE_PER_STEP, trend_value=pressure_effect_cp)
    new_car_data['coolant_pressure'] = np.clip(new_car_data['coolant_pressure'], 1.0, 1.6)

    # Oil Temperature
    stress_effect_ot = (new_car_data['engine_rpm'] - ENGINE_RPM_BASE) / 1000 * OIL_TEMP_STRESS_INCREASE
    new_car_data['oil_temperature'] = _apply_change(_last_car_data['oil_temperature'], OIL_TEMP_BASE, OIL_TEMP_NOISE_PER_STEP, trend_value=stress_effect_ot)
    new_car_data['oil_temperature'] = np.clip(new_car_data['oil_temperature'], 90, 115)

    # Oil Pressure
    rpm_effect_op = (new_car_data['engine_rpm'] - ENGINE_RPM_BASE) * OIL_PRESSURE_RPM_EFFECT
    level_effect_op = (1.0 - _current_oil_level) * OIL_PRESSURE_LEVEL_EFFECT * 100 # Larger effect as level drops
    new_car_data['oil_pressure'] = _apply_change(_last_car_data['oil_pressure'], OIL_PRESSURE_BASE, OIL_PRESSURE_NOISE_PER_STEP, trend_value=rpm_effect_op + level_effect_op)
    new_car_data['oil_pressure'] = np.clip(new_car_data['oil_pressure'], 40, 75)

    # Oil Level (gradually decreases)
    new_car_data['oil_level'] = _current_oil_level - OIL_LEVEL_DECREASE_PER_SECOND + np.random.uniform(-OIL_LEVEL_DECREASE_PER_SECOND/5, OIL_LEVEL_DECREASE_PER_SECOND/5)
    new_car_data['oil_level'] = np.clip(new_car_data['oil_level'], 0.7, 1.0) # Capped at 70% for dummy data

    # --- Driver Health ---
    fatigue_increase_per_second = HEART_RATE_FATIGUE_INCREASE_PER_HOUR / 3600
    stress_effect_hr = 0
    if brake_event or random.random() < ACCELERATION_EVENT_PROB: # Simulate driver stress on events
        stress_effect_hr = HEART_RATE_STRESS_SPIKE * np.random.uniform(0.5, 1.0)
    new_driver_data['heart_rate'] = _apply_change(_last_driver_data['heart_rate'], HEART_RATE_BASE, HEART_RATE_NOISE_PER_STEP, trend_value=fatigue_increase_per_second + stress_effect_hr)
    new_driver_data['heart_rate'] = np.clip(new_driver_data['heart_rate'], 100, 170)

    fatigue_increase_gsr_per_second = GSR_FATIGUE_INCREASE_PER_HOUR / 3600
    stress_effect_gsr = 0
    if brake_event or random.random() < ACCELERATION_EVENT_PROB:
        stress_effect_gsr = GSR_STRESS_SPIKE * np.random.uniform(0.5, 1.0)
    new_driver_data['gsr'] = _apply_change(_last_driver_data['gsr'], GSR_BASE, GSR_NOISE_PER_STEP, trend_value=fatigue_increase_gsr_per_second + stress_effect_gsr)
    new_driver_data['gsr'] = np.clip(new_driver_data['gsr'], 0, 12)

    fatigue_increase_pd_per_second = PUPIL_DILATION_FATIGUE_INCREASE_PER_HOUR / 3600
    light_effect_pd_val = (new_env_data['ambient_light'] - AMBIENT_LIGHT_BASE) * PUPIL_DILATION_LIGHT_EFFECT_FACTOR
    new_driver_data['pupil_dilation'] = _apply_change(_last_driver_data['pupil_dilation'], PUPIL_DILATION_BASE, PUPIL_DILATION_NOISE_PER_STEP, trend_value=fatigue_increase_pd_per_second + light_effect_pd_val)
    new_driver_data['pupil_dilation'] = np.clip(new_driver_data['pupil_dilation'], 3.0, 6.0)

    fatigue_decrease_br_per_second = BLINK_RATE_FATIGUE_DECREASE_PER_HOUR / 3600
    new_driver_data['blink_rate'] = _apply_change(_last_driver_data['blink_rate'], BLINK_RATE_BASE, BLINK_RATE_NOISE_PER_STEP, trend_value=-fatigue_decrease_br_per_second)
    new_driver_data['blink_rate'] = np.clip(new_driver_data['blink_rate'], 5, 20)


    # --- Update Global State for Next Call ---
    _current_oil_level = new_car_data['oil_level']
    _current_tire_wear = new_car_data['tire_wear_rate']
    _last_car_data = new_car_data
    _last_driver_data = new_driver_data
    _last_env_data = new_env_data

    # Combine all data into one row dictionary
    current_data_row = {
        **new_car_data,
        **new_driver_data,
        **new_env_data
    }

    return current_data_row

# --- Example Usage (How you would simulate the stream) ---
if __name__ == "__main__":
    simulation_duration_seconds = 3600
    output_filename = "simulated_realtime_race_data.csv"

    if len(sys.argv) > 1:
        try:
            simulation_duration_seconds = int(sys.argv[1])
            if simulation_duration_seconds <= 0:
                print("Duration must be a positive integer. Using default (3600s).")
                simulation_duration_seconds = 3600
        except ValueError:
            print("Invalid duration provided. Please provide an integer. Using default (3600s).")
            simulation_duration_seconds = 3600
    
    print(f"Simulating data stream for {simulation_duration_seconds} seconds...")

    initialize_race_data_stream()

    streamed_data = []
    for i in range(simulation_duration_seconds):
        data_point = generate_next_data_point()
        streamed_data.append(data_point)

    streamed_df = pd.DataFrame(streamed_data)
    
    print(f"\nData generation complete. Saved to '{output_filename}' with {len(streamed_df)} rows.")
    streamed_df.to_csv(output_filename, index=False)

    print("\nFirst 5 data points from the simulated stream:")
    print(streamed_df.head())
    print("\nLast 5 data points from the simulated stream:")
    print(streamed_df.tail())
    print("\nDescriptive statistics for a few columns from the streamed data:")
    print(streamed_df[['tire_temp_FL', 'heart_rate', 'blink_rate', 'rainfall_intensity', 'oil_level']].describe())