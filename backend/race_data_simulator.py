import pandas as pd
import numpy as np
import datetime
import random
import sys

# --- Helper Function (stateless, so can be outside the class or a static method) ---
def _apply_change(current_value, base_value, noise_range, trend_value=0, event_effect=0):
    """Applies a small random walk, a trend, and an event effect to a value, gravitating towards base."""
    new_value = current_value * 0.9 + base_value * 0.1 # Gravitate towards base
    new_value += np.random.uniform(-noise_range, noise_range)
    new_value += trend_value
    new_value += event_effect
    return new_value

class RaceDataSimulator:
    def __init__(self, num_hours=6, sample_rate_seconds=1, random_seed=None):
        """
        Initializes a new instance of the RaceDataSimulator.

        Args:
            num_hours (int): The total duration of the simulated data in hours.
            sample_rate_seconds (int): How frequently data points are sampled (in seconds).
            random_seed (int, optional): A seed for the random number generators
                                         to ensure reproducibility for this specific instance.
        """
        # --- Instance Configuration ---
        self.num_hours = num_hours
        self.sample_rate_seconds = sample_rate_seconds
        self.total_samples = self.num_hours * 3600 // self.sample_rate_seconds
        
        # Initialize random state for this instance
        # Using numpy.random.default_rng for modern NumPy random state management
        if random_seed is not None:
            self._rng_np = np.random.default_rng(random_seed)
            self._rng_random = random.Random(random_seed)
        else:
            self._rng_np = np.random.default_rng()
            self._rng_random = random.Random()

        # --- Instance-specific State Variables (formerly global) ---
        self._current_sample_index = 0
        self._current_oil_level = 100.0
        self._current_tire_wear = 0.0
        self._last_car_data = {}
        self._last_driver_data = {}
        self._last_env_data = {}
        self._start_time = None # Will be set during initialization

        # --- Realistic Parameter Ranges & Initial Values (now instance attributes) ---
        # Car State
        self.TIRE_TEMP_BASE = 90
        self.TIRE_TEMP_NOISE_PER_STEP = 1.0
        self.TIRE_PRESSURE_BASE = 30.0
        self.TIRE_PRESSURE_NOISE_PER_STEP = 0.1
        self.TIRE_WEAR_RATE_PER_SECOND = 0.000005

        self.BRAKE_DISC_TEMP_BASE = 400
        self.BRAKE_DISC_TEMP_NOISE_PER_STEP = 20
        self.BRAKE_DISC_TEMP_SPIKE_INCREMENT = 200
        self.BRAKE_DISC_TEMP_DECAY_RATE = 0.95

        self.BRAKE_PEDAL_PRESSURE_DECAY_RATE = 0.8
        self.BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP = 5

        self.ENGINE_RPM_BASE = 7000
        self.ENGINE_RPM_NOISE_PER_STEP = 100

        self.COOLANT_TEMP_BASE = 95
        self.COOLANT_TEMP_NOISE_PER_STEP = 0.5
        self.COOLANT_TEMP_STRESS_INCREASE = 0.5

        self.COOLANT_PRESSURE_BASE = 1.3
        self.COOLANT_PRESSURE_NOISE_PER_STEP = 0.01
        self.COOLANT_PRESSURE_TEMP_EFFECT = 0.02

        self.OIL_TEMP_BASE = 100
        self.OIL_TEMP_NOISE_PER_STEP = 0.5
        self.OIL_TEMP_STRESS_INCREASE = 0.8

        self.OIL_PRESSURE_BASE = 60
        self.OIL_PRESSURE_NOISE_PER_STEP = 0.5
        self.OIL_PRESSURE_RPM_EFFECT = 0.005
        self.OIL_PRESSURE_LEVEL_EFFECT = -0.1

        self.OIL_LEVEL_DECREASE_PER_SECOND = 0.000002

        # Driver Health
        self.HEART_RATE_BASE = 130
        self.HEART_RATE_NOISE_PER_STEP = 1.0
        self.HEART_RATE_FATIGUE_INCREASE_PER_HOUR = 2
        self.HEART_RATE_STRESS_SPIKE = 10

        self.GSR_BASE = 4
        self.GSR_NOISE_PER_STEP = 0.1
        self.GSR_FATIGUE_INCREASE_PER_HOUR = 0.2
        self.GSR_STRESS_SPIKE = 2

        self.PUPIL_DILATION_BASE = 4.5
        self.PUPIL_DILATION_NOISE_PER_STEP = 0.05
        self.PUPIL_DILATION_FATIGUE_INCREASE_PER_HOUR = 0.01
        self.PUPIL_DILATION_LIGHT_EFFECT_FACTOR = 0.00005

        self.BLINK_RATE_BASE = 18
        self.BLINK_RATE_NOISE_PER_STEP = 0.2
        self.BLINK_RATE_FATIGUE_DECREASE_PER_HOUR = 0.5

        # Environmental Condition
        self.RAINFALL_INTENSITY_NOISE_PER_STEP = 0.1
        self.RAINFALL_MAX_INTENSITY = 10.0
        self.RAINFALL_EVENT_DURATION_SECONDS = 3600 * 4
        self.RAINFALL_EVENT_START_SECOND = 3600 * 6

        self.TRACK_TEMP_BASE = 35
        self.TRACK_TEMP_NOISE_PER_STEP = 0.1
        self.TRACK_TEMP_RAIN_EFFECT = -5
        self.TRACK_TEMP_NIGHT_EFFECT_PER_HOUR = -0.5

        self.AMBIENT_LIGHT_BASE = 70000
        self.AMBIENT_LIGHT_NOISE_PER_STEP = 500
        self.AMBIENT_LIGHT_NIGHT_THRESHOLD = 500
        self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS = 3600 * 2
        self.AMBIENT_LIGHT_NIGHT_START_HOUR = 18
        self.AMBIENT_LIGHT_DAY_START_HOUR = 6

        # Event probabilities per second
        self.BRAKING_EVENT_PROB = 0.005
        self.ACCELERATION_EVENT_PROB = 0.002

        print(f"RaceDataSimulator instance created (Duration: {self.num_hours}h, Sample Rate: {self.sample_rate_seconds}s).")
        # Call initialization method to set up initial state
        self.initialize_simulation()

    def initialize_simulation(self):
        """Initializes the instance's internal state variables for a new simulation run."""
        self._current_sample_index = 0
        self._current_oil_level = 1.0 # Start at 1.0 (100%)
        self._current_tire_wear = 0.0
        self._start_time = datetime.datetime.now()

        # Set initial "last" data points to base values
        self._last_car_data = {
            'tire_temp_FL': self.TIRE_TEMP_BASE, 'tire_temp_FR': self.TIRE_TEMP_BASE, 'tire_temp_RL': self.TIRE_TEMP_BASE, 'tire_temp_RR': self.TIRE_TEMP_BASE,
            'tire_pressure_FL': self.TIRE_PRESSURE_BASE, 'tire_pressure_FR': self.TIRE_PRESSURE_BASE, 'tire_pressure_RL': self.TIRE_PRESSURE_BASE, 'tire_pressure_RR': self.TIRE_PRESSURE_BASE,
            'tire_wear_rate': 0.0,
            'brake_disc_temp_FL': self.BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_FR': self.BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_RL': self.BRAKE_DISC_TEMP_BASE, 'brake_disc_temp_RR': self.BRAKE_DISC_TEMP_BASE,
            'brake_pedal_pressure': 0.0,
            'engine_rpm': self.ENGINE_RPM_BASE,
            'coolant_temperature': self.COOLANT_TEMP_BASE,
            'coolant_pressure': self.COOLANT_PRESSURE_BASE,
            'oil_temperature': self.OIL_TEMP_BASE,
            'oil_pressure': self.OIL_PRESSURE_BASE,
            'oil_level': 1.0 # Current oil level will be used here to kick off
        }

        self._last_driver_data = {
            'heart_rate': self.HEART_RATE_BASE,
            'gsr': self.GSR_BASE,
            'pupil_dilation': self.PUPIL_DILATION_BASE,
            'blink_rate': self.BLINK_RATE_BASE
        }

        self._last_env_data = {
            'rainfall_intensity': 0.0,
            'track_temperature': self.TRACK_TEMP_BASE,
            'ambient_light': self.AMBIENT_LIGHT_BASE
        }
        print("Simulation state initialized for this instance.")


    def _generate_car_data(self, current_time_in_seconds, track_temperature_val):
        """Generates a single row of realistic car data for this instance."""
        data = {}

        # Engine RPM (random walk around base, occasional shifts)
        data['engine_rpm'] = _apply_change(self._last_car_data['engine_rpm'], self.ENGINE_RPM_BASE, self.ENGINE_RPM_NOISE_PER_STEP)
        if self._rng_random.random() < self.ACCELERATION_EVENT_PROB:
            data['engine_rpm'] = min(9500, data['engine_rpm'] + 1000)
        data['engine_rpm'] = np.clip(data['engine_rpm'], 5000, 9000)

        # Brake Pedal Pressure & Brake Disc Temp
        brake_event = False
        if self._rng_random.random() < self.BRAKING_EVENT_PROB:
            brake_event = True
            data['brake_pedal_pressure'] = self._rng_np.uniform(50, 100)
        else:
            data['brake_pedal_pressure'] = self._last_car_data['brake_pedal_pressure'] * self.BRAKE_PEDAL_PRESSURE_DECAY_RATE + self._rng_np.uniform(-self.BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP, self.BRAKE_PEDAL_PRESSURE_NOISE_PER_STEP)
            data['brake_pedal_pressure'] = max(0, data['brake_pedal_pressure'])

        for side in ['FL', 'FR', 'RL', 'RR']:
            temp_key = f'brake_disc_temp_{side}'
            new_val = self._last_car_data[temp_key] * self.BRAKE_DISC_TEMP_DECAY_RATE + self.BRAKE_DISC_TEMP_BASE * (1 - self.BRAKE_DISC_TEMP_DECAY_RATE)
            new_val += self._rng_np.uniform(-self.BRAKE_DISC_TEMP_NOISE_PER_STEP, self.BRAKE_DISC_TEMP_NOISE_PER_STEP)
            if brake_event:
                new_val += self.BRAKE_DISC_TEMP_SPIKE_INCREMENT * self._rng_np.uniform(0.8, 1.2)
            data[temp_key] = np.clip(new_val, self.BRAKE_DISC_TEMP_BASE * 0.7, self.BRAKE_DISC_TEMP_BASE * 1.8)

        # Tire Temps and Pressures
        for side in ['FL', 'FR', 'RL', 'RR']:
            temp_key = f'tire_temp_{side}'
            pressure_key = f'tire_pressure_{side}'
            
            engine_stress_factor = (data['engine_rpm'] - self.ENGINE_RPM_BASE) / (9000 - self.ENGINE_RPM_BASE) if (9000 - self.ENGINE_RPM_BASE) > 0 else 0
            brake_stress_factor = (data[f'brake_disc_temp_{side}'] - self.BRAKE_DISC_TEMP_BASE) / (self.BRAKE_DISC_TEMP_SPIKE_INCREMENT * 1.2) if (self.BRAKE_DISC_TEMP_SPIKE_INCREMENT * 1.2) > 0 else 0
            
            temp_trend = engine_stress_factor * 0.5 + brake_stress_factor * 0.5 + (track_temperature_val - self.TRACK_TEMP_BASE) * 0.1
            data[temp_key] = _apply_change(self._last_car_data[temp_key], self.TIRE_TEMP_BASE, self.TIRE_TEMP_NOISE_PER_STEP, trend_value=temp_trend)
            data[temp_key] = np.clip(data[temp_key], 70, 115)

            pressure_temp_effect = (data[temp_key] - self.TIRE_TEMP_BASE) * 0.01
            data[pressure_key] = _apply_change(self._last_car_data[pressure_key], self.TIRE_PRESSURE_BASE, self.TIRE_PRESSURE_NOISE_PER_STEP, trend_value=pressure_temp_effect)
            data[pressure_key] = np.clip(data[pressure_key], 28, 32)
            
        # Tire Wear Rate (gradually increases)
        data['tire_wear_rate'] = self._current_tire_wear + self.TIRE_WEAR_RATE_PER_SECOND + self._rng_np.uniform(-self.TIRE_WEAR_RATE_PER_SECOND/5, self.TIRE_WEAR_RATE_PER_SECOND/5)
        data['tire_wear_rate'] = np.clip(data['tire_wear_rate'], 0.0, 1.0)

        # Coolant Temperature
        stress_effect_ct = (data['engine_rpm'] - self.ENGINE_RPM_BASE) / 1000 * self.COOLANT_TEMP_STRESS_INCREASE
        data['coolant_temperature'] = _apply_change(self._last_car_data['coolant_temperature'], self.COOLANT_TEMP_BASE, self.COOLANT_TEMP_NOISE_PER_STEP, trend_value=stress_effect_ct)
        data['coolant_temperature'] = np.clip(data['coolant_temperature'], 85, 105)

        # Coolant Pressure
        pressure_effect_cp = (data['coolant_temperature'] - self.COOLANT_TEMP_BASE) * self.COOLANT_PRESSURE_TEMP_EFFECT
        data['coolant_pressure'] = _apply_change(self._last_car_data['coolant_pressure'], self.COOLANT_PRESSURE_BASE, self.COOLANT_PRESSURE_NOISE_PER_STEP, trend_value=pressure_effect_cp)
        data['coolant_pressure'] = np.clip(data['coolant_pressure'], 1.0, 1.6)

        # Oil Temperature
        stress_effect_ot = (data['engine_rpm'] - self.ENGINE_RPM_BASE) / 1000 * self.OIL_TEMP_STRESS_INCREASE
        data['oil_temperature'] = _apply_change(self._last_car_data['oil_temperature'], self.OIL_TEMP_BASE, self.OIL_TEMP_NOISE_PER_STEP, trend_value=stress_effect_ot)
        data['oil_temperature'] = np.clip(data['oil_temperature'], 90, 115)

        # Oil Pressure
        rpm_effect_op = (data['engine_rpm'] - self.ENGINE_RPM_BASE) * self.OIL_PRESSURE_RPM_EFFECT
        level_effect_op = (1.0 - self._current_oil_level) * self.OIL_PRESSURE_LEVEL_EFFECT * 100
        data['oil_pressure'] = _apply_change(self._last_car_data['oil_pressure'], self.OIL_PRESSURE_BASE, self.OIL_PRESSURE_NOISE_PER_STEP, trend_value=rpm_effect_op + level_effect_op)
        data['oil_pressure'] = np.clip(data['oil_pressure'], 40, 75)

        # Oil Level (gradually decreases)
        data['oil_level'] = self._current_oil_level - self.OIL_LEVEL_DECREASE_PER_SECOND + self._rng_np.uniform(-self.OIL_LEVEL_DECREASE_PER_SECOND/5, self.OIL_LEVEL_DECREASE_PER_SECOND/5)
        data['oil_level'] = np.clip(data['oil_level'], 0.7, 1.0)

        return data

    def _generate_driver_data(self, current_time_in_seconds, ambient_light_val, brake_event_happened, acceleration_event_happened):
        """Generates a single row of realistic driver data for this instance."""
        data = {}
        
        # Calculate fatigue factor based on total samples for this instance
        fatigue_factor = min(1.0, current_time_in_seconds / (self.total_samples * self.sample_rate_seconds) * 1.5)

        # Heart Rate (can vary with fatigue/stress)
        stress_effect_hr = 0
        if brake_event_happened or acceleration_event_happened: # Simulate driver stress on events
            stress_effect_hr = self.HEART_RATE_STRESS_SPIKE * self._rng_np.uniform(0.5, 1.0)
        data['heart_rate'] = _apply_change(self._last_driver_data['heart_rate'], self.HEART_RATE_BASE, self.HEART_RATE_NOISE_PER_STEP, trend_value=fatigue_factor * (self.HEART_RATE_FATIGUE_INCREASE_PER_HOUR / 3600) + stress_effect_hr)
        data['heart_rate'] = np.clip(data['heart_rate'], 100, 170)

        # GSR (Galvanic Skin Response - stress indicator)
        stress_effect_gsr = 0
        if brake_event_happened or acceleration_event_happened:
            stress_effect_gsr = self.GSR_STRESS_SPIKE * self._rng_np.uniform(0.5, 1.0)
        data['gsr'] = _apply_change(self._last_driver_data['gsr'], self.GSR_BASE, self.GSR_NOISE_PER_STEP, trend_value=fatigue_factor * (self.GSR_FATIGUE_INCREASE_PER_HOUR / 3600) + stress_effect_gsr)
        data['gsr'] = np.clip(data['gsr'], 0, 12)

        # Pupil Dilation (can increase slightly with fatigue, affected by light)
        fatigue_increase_pd_per_second = self.PUPIL_DILATION_FATIGUE_INCREASE_PER_HOUR / 3600
        light_effect_pd_val = (ambient_light_val - self.AMBIENT_LIGHT_BASE) * self.PUPIL_DILATION_LIGHT_EFFECT_FACTOR
        data['pupil_dilation'] = _apply_change(self._last_driver_data['pupil_dilation'], self.PUPIL_DILATION_BASE, self.PUPIL_DILATION_NOISE_PER_STEP, trend_value=fatigue_increase_pd_per_second + light_effect_pd_val)
        data['pupil_dilation'] = np.clip(data['pupil_dilation'], 3.0, 6.0)

        # Blink Rate (decreases with fatigue)
        fatigue_decrease_br_per_second = self.BLINK_RATE_FATIGUE_DECREASE_PER_HOUR / 3600
        data['blink_rate'] = _apply_change(self._last_driver_data['blink_rate'], self.BLINK_RATE_BASE, self.BLINK_RATE_NOISE_PER_STEP, trend_value=-fatigue_decrease_br_per_second)
        data['blink_rate'] = np.clip(data['blink_rate'], 5, 20)

        return data

    def _generate_environmental_data(self, current_time_in_seconds):
        """Generates a single row of realistic environmental data for this instance."""
        data = {}
        
        current_time_in_hours = current_time_in_seconds / 3600.0

        # Ambient Light (Day/Night Cycle)
        current_hour_in_day = current_time_in_hours % 24
        ambient_light_val = self.AMBIENT_LIGHT_BASE
        if self.AMBIENT_LIGHT_NIGHT_START_HOUR <= current_hour_in_day or current_hour_in_day < self.AMBIENT_LIGHT_DAY_START_HOUR:
            if self.AMBIENT_LIGHT_NIGHT_START_HOUR <= current_hour_in_day < self.AMBIENT_LIGHT_NIGHT_START_HOUR + self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600:
                transition_progress = (current_hour_in_day - self.AMBIENT_LIGHT_NIGHT_START_HOUR) / (self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600)
                ambient_light_val = np.interp(transition_progress, [0, 1], [self.AMBIENT_LIGHT_BASE, self.AMBIENT_LIGHT_NIGHT_THRESHOLD])
            elif current_hour_in_day >= self.AMBIENT_LIGHT_DAY_START_HOUR - self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600 and current_hour_in_day < self.AMBIENT_LIGHT_DAY_START_HOUR:
                transition_progress = (current_hour_in_day - (self.AMBIENT_LIGHT_DAY_START_HOUR - self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600)) / (self.AMBIENT_LIGHT_NIGHT_TRANSITION_SECONDS/3600)
                ambient_light_val = np.interp(transition_progress, [0, 1], [self.AMBIENT_LIGHT_NIGHT_THRESHOLD, self.AMBIENT_LIGHT_BASE])
            else:
                ambient_light_val = self.AMBIENT_LIGHT_NIGHT_THRESHOLD
        else:
            ambient_light_val = self.AMBIENT_LIGHT_BASE
            
        ambient_light_val += self._rng_np.uniform(-self.AMBIENT_LIGHT_NOISE_PER_STEP, self.AMBIENT_LIGHT_NOISE_PER_STEP)
        ambient_light_val = max(10, ambient_light_val)

        # Rainfall Intensity
        rainfall_intensity_val = 0.0
        if self.RAINFALL_EVENT_START_SECOND <= current_time_in_seconds < self.RAINFALL_EVENT_START_SECOND + self.RAINFALL_EVENT_DURATION_SECONDS:
            rain_progress = (current_time_in_seconds - self.RAINFALL_EVENT_START_SECOND) / self.RAINFALL_EVENT_DURATION_SECONDS
            if rain_progress < 0.1:
                rainfall_intensity_val = np.interp(rain_progress, [0, 0.1], [0, self.RAINFALL_MAX_INTENSITY * 0.8])
            else:
                rainfall_intensity_val = self._rng_np.uniform(self.RAINFALL_MAX_INTENSITY * 0.7, self.RAINFALL_MAX_INTENSITY)
        else:
            rainfall_intensity_val = max(0.0, self._last_env_data['rainfall_intensity'] * 0.99 - self._rng_np.uniform(0, self.RAINFALL_INTENSITY_NOISE_PER_STEP))
        rainfall_intensity_val = max(0.0, rainfall_intensity_val + self._rng_np.uniform(-self.RAINFALL_INTENSITY_NOISE_PER_STEP, self.RAINFALL_INTENSITY_NOISE_PER_STEP))

        # Track Temperature
        track_temp_trend = (ambient_light_val / self.AMBIENT_LIGHT_BASE - 0.5) * 10
        if rainfall_intensity_val > 0.5:
            track_temp_trend += self.TRACK_TEMP_RAIN_EFFECT
        data['track_temperature'] = _apply_change(self._last_env_data['track_temperature'], self.TRACK_TEMP_BASE, self.TRACK_TEMP_NOISE_PER_STEP, trend_value=track_temp_trend/3600)
        data['track_temperature'] = np.clip(data['track_temperature'], 10, 50)
        
        data['rainfall_intensity'] = rainfall_intensity_val
        data['ambient_light'] = ambient_light_val

        return data

    def generate_next_data_point(self):
        """
        Generates a single, new data point for this instance, based on its previous state.
        Increments the internal sample index and updates the instance's state for the next call.
        Returns a dictionary of the new data point.
        """
        # Increment the sample index for this instance
        self._current_sample_index += 1
        
        current_time_in_seconds = self._current_sample_index * self.sample_rate_seconds

        # Generate environmental data first, as car data might depend on it
        env_data = self._generate_environmental_data(current_time_in_seconds)
        
        # Determine if a brake/acceleration event happened this step
        # These are used for driver stress calculation and are randomly determined here
        brake_event_happened = self._rng_random.random() < self.BRAKING_EVENT_PROB
        acceleration_event_happened = self._rng_random.random() < self.ACCELERATION_EVENT_PROB

        # Generate car data
        car_data = self._generate_car_data(current_time_in_seconds, env_data['track_temperature'])
        
        # Generate driver data, passing event flags and ambient light
        driver_data = self._generate_driver_data(
            current_time_in_seconds,
            env_data['ambient_light'],
            brake_event_happened,
            acceleration_event_happened
        )

        # Update instance state for next iteration
        self._current_oil_level = car_data['oil_level']
        self._current_tire_wear = car_data['tire_wear_rate']
        self._last_car_data = car_data
        self._last_driver_data = driver_data
        self._last_env_data = env_data

        # Combine all data into one row dictionary
        current_data_row = {
            **car_data,
            **driver_data,
            **env_data
        }

        return current_data_row

    def generate_full_dataset(self):
        """
        Generates a complete dataset for this instance based on its configuration.
        Returns a pandas DataFrame.
        This method will also re-initialize the simulation state before generating.
        """
        print(f"Generating {self.total_samples} data points over {self.num_hours} hours at {self.sample_rate_seconds}-second intervals for this instance...")

        data_rows = []
        # Re-initialize state to ensure a fresh start for full dataset generation
        self.initialize_simulation()

        for _ in range(self.total_samples):
            # Call generate_next_data_point without parameters
            data_point = self.generate_next_data_point()
            data_rows.append(data_point)

        df = pd.DataFrame(data_rows)
        return df

# --- Example Usage (How you would create and use multiple instances) ---
if __name__ == "__main__":
    # --- Instance 1: Default Simulation (6 hours) ---
    print("--- Running Simulation Instance 1 (Default: 6 hours) ---")
    generator1 = RaceDataSimulator() # Uses default 6 hours, 1 second sample rate
    df1 = generator1.generate_full_dataset()
    output_filename1 = "race_data_instance_1.csv"
    df1.to_csv(output_filename1, index=False)
    print(f"\nData for instance 1 saved to '{output_filename1}' with {len(df1)} rows.")
    print("\nFirst 5 rows of Instance 1 data:")
    print(df1.head())
    print("\nDescriptive statistics for a few columns from Instance 1 data:")
    print(df1[['tire_temp_FL', 'heart_rate', 'blink_rate', 'rainfall_intensity', 'oil_level']].describe())
    print("-" * 50)