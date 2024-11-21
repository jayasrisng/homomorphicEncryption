import seal
import pandas as pd
import os


def test_seal_environment(chunk1_path):
    try:
        # Dynamically find the first user folder
        print(f"Scanning folder: {chunk1_path}")
        user_folders = [os.path.join(chunk1_path, folder) for folder in os.listdir(chunk1_path) if
                        os.path.isdir(os.path.join(chunk1_path, folder))]

        if not user_folders:
            print("No user folders found in the specified path!")
            return False

        print(f"Found {len(user_folders)} user folders. Selecting the first one for testing...")
        sample_user_folder = user_folders[0]  # Select the first user folder

        # Find a normalized CSV file in the selected user folder
        normalized_files = [file for file in os.listdir(sample_user_folder) if
                            "normalized" in file and file.endswith(".csv")]

        if not normalized_files:
            print(f"No normalized CSV files found in the folder: {sample_user_folder}")
            return False

        sample_file_path = os.path.join(sample_user_folder, normalized_files[0])
        print(f"Using sample file: {sample_file_path}")

        # Load the normalized CSV file
        print("Loading sample data...")
        data = pd.read_csv(sample_file_path)

        # Verify data structure
        if data.empty or "saberSpeed" not in data.columns:
            print("Sample data is empty or does not contain 'saberSpeed' column!")
            return False

        print("Sample data loaded successfully.")
        print("Sample Data Preview:")
        print(data.head())

        # Encryption parameters
        print("Setting up encryption parameters...")
        parms = seal.EncryptionParameters(seal.scheme_type.ckks)
        poly_modulus_degree = 8192
        parms.set_poly_modulus_degree(poly_modulus_degree)
        parms.set_coeff_modulus(seal.CoeffModulus.Create(poly_modulus_degree, [60, 40, 40, 60]))

        scale = 2 ** 40
        context = seal.SEALContext(parms)
        print("Encryption parameters set.")

        # Initialize CKKS Encoder
        ckks_encoder = seal.CKKSEncoder(context)
        slot_count = ckks_encoder.slot_count()
        print(f"CKKS slot count: {slot_count}")

        # Create keys and encryptor/decryptor
        keygen = seal.KeyGenerator(context)
        public_key = keygen.create_public_key()  # Adjusted method to create public key
        secret_key = keygen.secret_key()
        encryptor = seal.Encryptor(context, public_key)
        evaluator = seal.Evaluator(context)
        decryptor = seal.Decryptor(context, secret_key)

        # Encrypt a single column (saberSpeed)
        print("Encrypting 'saberSpeed' column...")
        saber_speed = data["saberSpeed"].values  # Extract values as numpy array

        # Split data into chunks that fit within the slot count
        batches = [saber_speed[i:i + slot_count] for i in range(0, len(saber_speed), slot_count)]

        # Encrypt each batch
        encrypted_batches = []
        for batch_index, batch in enumerate(batches):
            print(f"Encoding batch {batch_index + 1}/{len(batches)}...")
            encoded_data = ckks_encoder.encode(batch, scale)  # Encode the batch
            encrypted_data = encryptor.encrypt(encoded_data)  # Encrypt directly
            encrypted_batches.append(encrypted_data)  # Store the encrypted data

        print(f"Encrypted {len(encrypted_batches)} batches successfully.")

        # Decrypt one batch as an example
        print("Decrypting the first batch...")
        decrypted_result = decryptor.decrypt(encrypted_batches[0])  # Decrypt directly

        # Decode the result
        decoded_result = ckks_encoder.decode(decrypted_result)
        print(f"Decrypted data (first batch): {decoded_result[:5]} (showing first 5 values)")

        print("Environment test completed successfully!")
        return True

    except Exception as e:
        print(f"Error occurred during SEAL environment test: {e}")
        return False


# Path to chunk1 folder
chunk1_path = r"C:\Users\jguthula\Documents\chunk1"

# Run the test
is_ready = test_seal_environment(chunk1_path)
if is_ready:
    print("\nYour environment is ready for Microsoft SEAL.")
else:
    print("\nEnvironment setup is incomplete or encountered errors.")
