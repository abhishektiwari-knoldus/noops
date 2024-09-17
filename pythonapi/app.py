from flask import Flask, jsonify
import subprocess
from flask_cors import CORS
import json
import threading
import time
 

app = Flask(__name__)
CORS(app)

# Function to run terraform destroy after 5 minutes
def destroy_after_delay():
    time.sleep(300)
    
    try:
        destroy_result = subprocess.run(["terraform", "destroy", "--auto-approve"], check=True, text=True, capture_output=True)
        print("Terraform destroy successful:", destroy_result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error during terraform destroy: {e}")
 

@app.route('/run-terraform', methods=['POST'])
def run_terraform():
    try:
        # Run terraform init
        init_result = subprocess.run(["terraform", "init"], check=True, text=True, capture_output=True)
        plan_result = subprocess.run(["terraform", "plan"], text=True, capture_output=True)
        print(init_result.stdout)
        
        # Run terraform apply with auto-approval
        apply_result = subprocess.run(["terraform", "apply", "--auto-approve"], text=True, capture_output=True)
        output_result = subprocess.run(["terraform", "output", "-json"], capture_output=True, text=True)

        output = json.loads(output_result.stdout)


        bucket_url = output.get("bucket_url", {}).get("value", "No URL found")
          
        # Start the background thread to destroy the resources after 5 minutes  
        destroy_thread = threading.Thread(target=destroy_after_delay)
        destroy_thread.start()

        # Return the output as JSON
        return jsonify({
            "status": "success",
            "message": "Terraform apply successful",
            "bucket_url": bucket_url
        }), 200

    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)

    
    

