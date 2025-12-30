from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Bills folder path
BILLS_FOLDER = 'bills'

# Create bills folder if it doesn't exist
if not os.path.exists(BILLS_FOLDER):
    os.makedirs(BILLS_FOLDER)
    print(f"Created '{BILLS_FOLDER}' folder")

@app.route('/save-bill', methods=['POST'])
def save_bill():
    try:
        # Get the PDF file and metadata
        pdf_file = request.files.get('pdf')
        receipt_no = request.form.get('receiptNo', '').strip()
        received_from = request.form.get('receivedFrom', '').strip()
        
        if not pdf_file:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        if not receipt_no:
            return jsonify({'error': 'Receipt number is required'}), 400
        
        if not received_from:
            return jsonify({'error': 'Recipient name is required'}), 400
        
        clean_receipt_no = "".join(c for c in receipt_no if c.isalnum() or c in ('-', '_'))
        clean_name = "".join(c for c in received_from if c.isalnum() or c in (' ', '-', '_'))
        clean_name = clean_name.replace(' ', '_')
        
        # Create filename: receiptNo_name.pdf
        filename = f"{clean_receipt_no}_{clean_name}.pdf"
        filepath = os.path.join(BILLS_FOLDER, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            # Add timestamp to make it unique
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{clean_receipt_no}_{clean_name}_{timestamp}.pdf"
            filepath = os.path.join(BILLS_FOLDER, filename)
        
        # Save the PDF file
        pdf_file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'path': filepath
        }), 200
        
    except Exception as e:
        print(f"Error saving bill: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'bills_folder': BILLS_FOLDER}), 200

if __name__ == '__main__':
    print("="*50)
    print("Money Receipt Backend Server")
    print("="*50)
    print(f"Bills will be saved in: {os.path.abspath(BILLS_FOLDER)}")
    print("Server running on: http://localhost:5000")
    print("="*50)
    app.run(debug=True, port=5000)
