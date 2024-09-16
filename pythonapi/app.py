from flask import Flask, jsonify
import subprocess
from flask_cors import CORS
import json
 

app = Flask(__name__)
CORS(app)
 

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

            # Return the output as JSON
        return jsonify({
            "bucket_url": output.get("bucket_url", {}).get("value", "No URL found")
        })


        if "Apply complete! Resources:" in apply_result.stdout:

            return jsonify({"status": "success", "message": "Terraform Successful"}), 200
        else:
            return jsonify({"status": "error", "message": "Terraform apply failed or had changes."}), 500
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)

    
    

