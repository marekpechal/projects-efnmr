import json
import time


class DataHandler:
    def __init__(self):
        self.current_data = None

    def save_data(self, data, filename=None):
        """Save data to a file"""
        if filename is None:
            timestamp = time.time()
            filename = f"nmr_data_{timestamp}.json"

        self.current_data = data

        # Convert array data to lists for JSON serialization
        try:
            if isinstance(data, list) and all(isinstance(x, list) for x in data):
                serializable_data = data  # CPMG multi-echo data
            else:
                serializable_data = list(data)  # Single echo data

            with open(filename, "w") as f:
                json.dump({"timestamp": time.time(), "data": serializable_data}, f)
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    # TODO: Place holder
    def send_data_serial(self, data, max_points=100):
        """Send data via serial connection (simplified)"""
        print("Serial data transfer:")
        if isinstance(data, list) and all(isinstance(x, list) for x in data):
            # For CPMG multi-echo data, print first few points of each echo
            for i, echo in enumerate(data):
                if i < 3:  # Just show first 3 echoes
                    print(f"Echo {i + 1}: {echo[:10]}...")
        # For single echo, print first few points
        else:
            print(f"Data: {list(data)[:max_points]}...")
