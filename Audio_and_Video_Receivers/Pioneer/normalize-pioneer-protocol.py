#!/usr/bin/env python3
import sys
import os

def process_file(input_file):
    # Create output filename based on input
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_processed{ext or '.txt'}"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Only process lines starting with "data:"
            if line.strip().startswith("data:"):
                parts = line.strip().split()
                new_parts = [parts[0]]  # keep "data:"
                for part in parts[1:]:
                    try:
                        num = float(part)

                        # I used numbers from: https://github.com/DarkFlippers/unleashed-firmware/blob/0530eda8d1df81768c72dbdf51d3e4c8c94148e6/lib/infrared/encoder_decoder/pioneer/infrared_protocol_pioneer_i.h

                        # replacement: 380–650 -> 500
                        if 380 <= num <= 650:
                            new_parts.append("500")
                        # replacement: 1380-1620 -> 1500
                        elif 1380 <= num <= 1620:
                            new_parts.append("1500")
                        # replacement: 4025-4425 -> 4225
                        elif 4025 <= num <= 4425:
                            new_parts.append("4225")
                        # replacement: 8300–8700 -> 8500
                        elif 8300 <= num <= 8700:
                            new_parts.append("8500")
                        # replacement: 24700–27600 -> 26000
                        elif 24700 <= num <= 27600:
                            new_parts.append("26000")
                        else:
                            # Keep original formatting (int vs float)
                            new_parts.append(str(int(num)) if num.is_integer() else str(num))
                    except ValueError:
                        # Not a number? leave as is
                        new_parts.append(part)

                outfile.write(" ".join(new_parts) + "\n")
            else:
                # Non-data lines: write unchanged
                outfile.write(line)

    print(f"Processing complete. Output written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_data_file.py <input_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    process_file(input_path)
