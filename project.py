import sys
import os
import json
import http.server
import webbrowser
import threading

def main():
    # ANSI escape characters for premium CLI styling
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    red = "\033[91m"
    bold = "\033[1m"
    reset = "\033[0m"

    print(f"\n{bold}{cyan}============================================={reset}")
    print(f"{bold}{cyan}     AUTOMATED FITNESS PROGRESS LOGGER       {reset}")
    print(f"{bold}{cyan}============================================={reset}")
    print(f"{bold}1.{reset} Enter a workout line manually")
    print(f"{bold}2.{reset} Load workouts from a text file")
    print(f"{bold}3.{reset} {green}{bold}Launch Web Dashboard (Visual & Elegant) [Web]{reset}")
    print(f"{bold}{cyan}--------------------------------------------={reset}")
    
    choice = input(f"{bold}Select an option (1, 2, or 3): {reset}").strip()
    workout_entries = []
    
    if choice == "1":
        print(f"\n{yellow}Enter data format: YYYY-MM-DD, Exercise, Sets, Reps, Weight{reset}")
        print(f"Example: {green}2026-06-27, Back Squat, 4, 8, 100{reset}")
        line = input("=> ").strip()
        try:
            parsed = parse_workout_line(line)
            workout_entries.append(parsed)
        except ValueError as e:
            sys.exit(f"{red}Error: {e}{reset}")
            
    elif choice == "2":
        filename = input(f"{bold}Enter log filename [default: workout_log.txt]: {reset}").strip()
        if not filename:
            filename = "workout_log.txt"
        try:
            with open(filename, "r") as file:
                for line_num, line in enumerate(file, 1):
                    cleaned_line = line.strip()
                    if not cleaned_line or cleaned_line.startswith("#"):
                        continue  # Skip empty lines or comments
                    try:
                        parsed = parse_workout_line(cleaned_line)
                        workout_entries.append(parsed)
                    except ValueError as e:
                        print(f"{yellow}Skipping line {line_num} due to error: {e}{reset}")
        except FileNotFoundError:
            sys.exit(f"{red}Error: The file '{filename}' could not be found.{reset}")
            
    elif choice == "3":
        start_web_server()
        return
        
    else:
        sys.exit(f"{red}Invalid selection. Exiting.{reset}")

    # Calculate and attach total volume for context before summary display
    print(f"\n{bold}{magenta}--- Summary Report ---{reset}")
    print(f"{cyan}{format_summary(workout_entries)}{reset}")
    
    if workout_entries:
        total_session_volume = sum(
            calculate_volume(w["sets"], w["reps"], w["weight"]) for w in workout_entries
        )
        print(f"\n{green}{bold}Total Session Volume Calculated: {total_session_volume:.2f} kg{reset}")

def parse_workout_line(line):
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 5:
        raise ValueError("Invalid format. Must contain: Date, Exercise, Sets, Reps, Weight")
    date, exercise, sets_str, reps_str, weight_str = parts
    if len(date) != 10 or date[4] != '-' or date[7] != '-':
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    if not exercise:
        raise ValueError("Exercise name cannot be empty")
    try:
        sets = int(sets_str)
        reps = int(reps_str)
        weight = float(weight_str)
    except ValueError:
        raise ValueError("Sets, Reps, and Weight must be numeric values")
    if sets <= 0 or reps <= 0 or weight < 0:
        raise ValueError("Sets and reps must be positive; weight cannot be negative")
    return {"date": date, "exercise": exercise, "sets": sets, "reps": reps, "weight": weight}

def calculate_volume(sets, reps, weight, unit="kg"):
    if sets <= 0 or reps <= 0 or weight < 0:
        raise ValueError("Invalid metrics for volume calculation")
    normalized_weight = weight
    if unit.lower() == "lbs":
        normalized_weight = weight * 0.45359237
    return round(sets * reps * normalized_weight, 2)

def format_summary(workout_data):
    if not workout_data:
        return "No workout entries found."
    header = f"{'Date':<12} | {'Exercise':<25} | {'Sets':<5} | {'Reps':<5} | {'Weight':<8}"
    separator = "-" * len(header)
    lines = [header, separator]
    for entry in workout_data:
        row = (
            f"{entry['date']:<12} | "
            f"{entry['exercise']:<25} | "
            f"{entry['sets']:<5} | "
            f"{entry['reps']:<5} | "
            f"{entry['weight']:<8.1f}"
        )
        lines.append(row)
    return "\n".join(lines)


# --- Visual Dashboard Web Server Implementation ---

class WorkoutHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging request noise to keep the server console clean
        pass

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                # Find path to index.html relative to this file
                dir_path = os.path.dirname(os.path.realpath(__file__))
                file_path = os.path.join(dir_path, "web", "index.html")
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(f"Error loading dashboard page: {e}".encode())
                
        elif self.path == "/api/workouts":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            workouts = []
            filename = "workout_log.txt"
            if os.path.exists(filename):
                try:
                    with open(filename, "r") as file:
                        for line in file:
                            cleaned_line = line.strip()
                            if not cleaned_line or cleaned_line.startswith("#"):
                                continue
                            try:
                                parsed = parse_workout_line(cleaned_line)
                                # Calculate volume in kg for standard dashboard logic
                                vol = calculate_volume(parsed["sets"], parsed["reps"], parsed["weight"])
                                parsed["volume"] = vol
                                workouts.append(parsed)
                            except ValueError:
                                continue
                except Exception:
                    pass
            self.wfile.write(json.dumps(workouts).encode())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/api/workouts/save":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                lines = data.get("lines", [])
                
                filename = "workout_log.txt"
                with open(filename, "w") as file:
                    file.write("# Automated Fitness Progress Log\n")
                    file.write("# Format: YYYY-MM-DD, Exercise, Sets, Reps, Weight\n")
                    for line in lines:
                        file.write(f"{line}\n")
                        
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
        else:
            self.send_error(404)

def start_web_server():
    port = 8000
    server_address = ('', port)
    handler = WorkoutHTTPRequestHandler
    
    # Try to bind to an available port
    max_tries = 10
    httpd = None
    for i in range(max_tries):
        try:
            httpd = http.server.HTTPServer(server_address, handler)
            break
        except OSError:
            port += 1
            server_address = ('', port)
            
    if not httpd:
        print("\033[91mError: Could not start web server. Ports 8000-8009 are already in use.\033[0m")
        return
        
    url = f"http://localhost:{port}"
    print("\n" + "="*60)
    print(f"\033[92m[+] Web Dashboard Server started successfully!\033[0m")
    print(f"Local Link: \033[94m\033[4m{url}\033[0m")
    print("The dashboard will automatically open in your web browser.")
    print("Press Ctrl+C in this terminal window to stop the server.")
    print("="*60 + "\n")
    
    # Delayed browser open to ensure server is listening
    def open_browser():
        webbrowser.open(url)
    
    threading.Timer(0.8, open_browser).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[93mShutting down web server... Goodbye!\033[0m")
        httpd.server_close()

if __name__ == "__main__":
    main()