import sys
import json

def to_vcf_string(first_name, last_name, phone):
    vcf_lines = [
        'BEGIN:VCARD',
        'VERSION:2.1',
        f'N:;{last_name};{first_name};;;',
        f'FN:{first_name}{" " if last_name else ""}{last_name}',
        f'TEL;CELL;PREF:{phone}',
        'END:VCARD'
    ]
    return '\n'.join(vcf_lines) + '\n'

def main(input_file, output_file_path):
    try:
        # Open the JSON file with the correct encoding
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        contacts_list = data.get('contacts', {}).get('list', [])
        
        # Open the output file for writing, ensuring it uses UTF-8 encoding
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for contact in contacts_list:
                first_name = contact.get('first_name', '')
                last_name = contact.get('last_name', '')
                phone = contact.get('phone_number', '')
                
                # Skip contacts with no name
                if not first_name and not last_name:
                    continue
                
                vcf_string = to_vcf_string(first_name, last_name, phone)
                output_file.write(vcf_string)
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
    except FileNotFoundError as e:
        print(f"Input file not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.json output.vcf")
    else:
        input_file = sys.argv[1]
        output_file_path = sys.argv[2]
        main(input_file, output_file_path)
