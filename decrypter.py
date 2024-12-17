import os
import subprocess

TOOL_PATH = "/Users/abht/Desktop/LogDecrypter/Mac"

def decrypt_log(encrypted_file_path, decrypted_filename):
    try:
        # Ensure the tool path exists
        if not os.path.exists(TOOL_PATH):
            raise FileNotFoundError(f"The specified tool path does not exist: {TOOL_PATH}")
        
        # Ensure encrypted file exists
        if not os.path.exists(encrypted_file_path):
            raise FileNotFoundError(f"Encrypted file not found: {encrypted_file_path}")
        
        # Construct the full decrypted file path
        decrypted_filepath = os.path.join(TOOL_PATH, decrypted_filename)
        
        # Print debugging information
        # print(f"Tool path: {TOOL_PATH}")
        print(f"Encrypted file path: {encrypted_file_path}")
        print(f"Decrypted file path: {decrypted_filepath}")
        
        # Change to the tool's directory
        os.chdir(TOOL_PATH)
        # print(f"Current working directory: {os.getcwd()}")
        
        # Construct and run the decryption command
        command = f"./LogDecrypter {encrypted_file_path} >> {decrypted_filepath}"
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # # Check the command's output
        # print(f"Command stdout: {result.stdout}")
        # print(f"Command stderr: {result.stderr}")
        
        if result.returncode != 0:
            raise RuntimeError(f"Decryption command failed: {result.stderr}")
        
        # Verify the decrypted file exists
        if not os.path.exists(decrypted_filepath):
            raise FileNotFoundError(f"Decrypted file was not created: {decrypted_filepath}")
        
        print(f"Decrypted file created successfully: {decrypted_filepath}")
        return decrypted_filepath
    except Exception as e:
        raise RuntimeError(f"Decryption failed: {e}")
