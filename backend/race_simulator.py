import random
import time

class DriverRaceSimulator:
    def __init__(self, driver_name: str = "Driver 1", car_name: str = "Car 1", starting_position: int = 10):
        """
        Initialize single driver race simulator
        
        Args:
            driver_name: Name of the driver
            car_name: Name/number of the car
            starting_position: Starting grid position
        """
        self.driver_name = driver_name
        self.car_name = car_name
        self.current_time = 0
        self.lap_length_seconds = 90  # Average lap time in seconds
        
        # Driver race data
        self.pic = starting_position  # Position in Classification
        self.laps = 0
        self.last_lap = 0.0
        self.best_lap = float('inf')
        self.gap = random.uniform(5, 25) if starting_position > 1 else 0.0  # Gap to leader
        self.pits = 0
        self.max_speed = random.uniform(280, 320)  # km/h
        
        # Internal tracking variables
        self.lap_start_time = 0
        self.base_lap_time = random.uniform(85, 95)  # Base lap time variation
        self.pit_stop_due = random.randint(1200, 2400)  # When pit stop is due (seconds)
        self.in_pit = False
        self.pit_time_remaining = 0
        self.stint_start_time = 0
        self.position_trend = 0  # Tracks if driver is gaining/losing positions
    
    def _calculate_lap_time(self) -> float:
        """Calculate realistic lap time with variation"""
        base_time = self.base_lap_time
        
        # Add random variation (±2 seconds)
        variation = random.uniform(-2, 2)
        
        # Tire degradation effect (slower as stint progresses)
        stint_length = self.current_time - self.stint_start_time
        degradation = min(stint_length / 1000, 3)  # Max 3s degradation
        
        # Weather/track conditions
        conditions = random.uniform(-1, 1)
        
        # Performance variation (driver having good/bad day)
        performance = random.uniform(-0.5, 0.5)
        
        return max(base_time + variation + degradation + conditions + performance, 75)
    
    def _handle_pit_stop(self):
        """Handle pit stop logic"""
        if self.in_pit:
            self.pit_time_remaining -= 1
            if self.pit_time_remaining <= 0:
                # Exit pit
                self.in_pit = False
                self.pits += 1
                self.stint_start_time = self.current_time
                self.pit_stop_due = self.current_time + random.randint(1200, 2400)
                # Lose positions during pit stop
                self.pic = min(self.pic + random.randint(3, 8), 20)
        elif self.current_time >= self.pit_stop_due and not self.in_pit:
            # Enter pit
            self.in_pit = True
            self.pit_time_remaining = random.randint(20, 30)  # 20-30 second pit stop
    
    def _update_position(self):
        """Update race position with realistic changes"""
        if self.in_pit:
            return
        
        # Position changes based on performance and race dynamics
        position_change_chance = 0.05  # 5% chance per second
        
        if random.random() < position_change_chance:
            # Determine if gaining or losing position
            performance_factor = random.uniform(-1, 1)
            
            if performance_factor > 0.3 and self.pic > 1:
                # Gain position (overtake)
                self.pic -= 1
                self.position_trend = 1
            elif performance_factor < -0.3 and self.pic < 20:
                # Lose position (get overtaken)
                self.pic += 1
                self.position_trend = -1
            else:
                self.position_trend = 0
    
    def _update_gap(self):
        """Update gap to leader based on position and performance"""
        if self.pic == 1:
            self.gap = 0.0
        else:
            # Gap changes based on relative performance
            gap_change = random.uniform(-0.5, 0.5)
            
            # Position influence on gap
            if self.position_trend == 1:  # Gaining positions
                gap_change -= random.uniform(0.2, 0.8)
            elif self.position_trend == -1:  # Losing positions
                gap_change += random.uniform(0.2, 0.8)
            
            # Pit stop impact
            if self.in_pit:
                gap_change += 1.0
            
            self.gap = max(0.0, self.gap + gap_change)
    
    def _update_max_speed(self):
        """Update max speed with realistic variation"""
        # Occasional speed updates (not every second)
        if random.random() < 0.1:  # 10% chance per second
            speed_variation = random.uniform(-5, 5)
            self.max_speed = max(min(self.max_speed + speed_variation, 340), 250)
    
    def generate_next_data_point(self) -> dict:
        """
        Generate next data point (1 second update)
        
        Returns:
            Dictionary with all race data including status information
        """
        self.current_time += 1
        
        # Handle pit stops
        self._handle_pit_stop()
        
        # Skip lap updates if in pit
        if not self.in_pit:
            # Check if lap is completed
            time_since_lap_start = self.current_time - self.lap_start_time
            expected_lap_time = self.base_lap_time
            
            if time_since_lap_start >= expected_lap_time:
                # Complete the lap
                actual_lap_time = self._calculate_lap_time()
                self.last_lap = actual_lap_time
                self.laps += 1
                self.lap_start_time = self.current_time
                
                # Update best lap
                if actual_lap_time < self.best_lap:
                    self.best_lap = actual_lap_time
            
            # Update position
            self._update_position()
        
        # Update gap and max speed
        self._update_gap()
        self._update_max_speed()
        
        # Calculate additional info
        elapsed_minutes = self.current_time // 60
        elapsed_seconds = self.current_time % 60
        
        # Return all race data
        return {
            'PiC': self.pic,
            'car_name': self.car_name,
            'laps': self.laps,
            'last_lap': round(self.last_lap, 3) if self.last_lap > 0 else 0.0,
            'best_lap': round(self.best_lap, 3) if self.best_lap != float('inf') else 0.0,
            'gap': round(self.gap, 3),
            'pits': self.pits,
            'max_speed': round(self.max_speed, 1),
            'driver_name': self.driver_name,
            'race_time': f"{elapsed_minutes:02d}:{elapsed_seconds:02d}",
            'status': 'PIT' if self.in_pit else 'RUNNING',
            'pit_time_remaining': self.pit_time_remaining if self.in_pit else 0,
            'next_pit_in': max(0, self.pit_stop_due - self.current_time) if not self.in_pit else 0
        }
    


# Example usage
if __name__ == "__main__":
    # Create driver simulator
    driver = DriverRaceSimulator("Lewis Hamilton", "Mercedes #44", starting_position=5)
    
    print(f"Race Simulation Started for {driver.driver_name} in {driver.car_name}!")
    print("=" * 70)
    
    # Simulate race updates
    for update in range(300):  # Simulate 5 minutes
        data = driver.generate_next_data_point()
        
        # Print update every 30 seconds
        if update % 30 == 0:
            print(f"\nRace Time: {data['race_time']} | Status: {data['status']}")
            if data['status'] == 'PIT':
                print(f"Pit time remaining: {data['pit_time_remaining']}s")
            else:
                print(f"Next pit stop in: {data['next_pit_in']}s")
            
            print("-" * 70)
            print(f"Position: P{data['PiC']}")
            print(f"Car: {data['car_name']}")
            print(f"Laps: {data['laps']}")
            print(f"Last Lap: {data['last_lap']}s")
            print(f"Best Lap: {data['best_lap']}s")
            print(f"Gap to Leader: +{data['gap']}s")
            print(f"Pit Stops: {data['pits']}")
            print(f"Max Speed: {data['max_speed']} km/h")
        
        # Small delay for real-time feel (remove for faster simulation)
        time.sleep(0.01)
    
    print(f"\nSimulation Complete for {driver.driver_name}!")