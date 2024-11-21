import seal
import pandas as pd
import os


def encrypt_all_users(chunk1_path):
    try:
        # Dynamically find all user folders
        print(f"Scanning folder: {chunk1_path}")
        user_folders = [os.path.join(chunk1_path, folder) for folder in os.listdir(chunk1_path) if
                        os.path.isdir(os.path.join(chunk1_path, folder))]

        if not user_folders:
            print("No user folders found in the specified path!")
            return False

        print(f"Found {len(user_folders)} user folders. Starting encryption for all users...")

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
        public_key = keygen.create_public_key()
        secret_key = keygen.secret_key()
        encryptor = seal.Encryptor(context, public_key)
        evaluator = seal.Evaluator(context)
        decryptor = seal.Decryptor(context, secret_key)

        # Iterate through all user folders
        for user_index, user_folder in enumerate(user_folders, start=1):
            print(f"Processing user {user_index}/{len(user_folders)}: {os.path.basename(user_folder)}")

            # Find normalized CSV files in the user folder
            normalized_files = [file for file in os.listdir(user_folder) if
                                "normalized" in file and file.endswith(".csv")]

            if not normalized_files:
                print(f"No normalized CSV files found in the folder: {user_folder}. Skipping...")
                continue

            # Process each file in the user's folder
            for normalized_file in normalized_files:
                file_path = os.path.join(user_folder, normalized_file)
                print(f"Encrypting file: {file_path}")

                # Load the normalized CSV file
                data = pd.read_csv(file_path)

                # Verify data structure
                if data.empty or "saberSpeed" not in data.columns:
                    print(f"File {normalized_file} is empty or does not contain 'saberSpeed'. Skipping...")
                    continue

                # Encrypt the saberSpeed column
                saber_speed = data["saberSpeed"].values
                batches = [saber_speed[i:i + slot_count] for i in range(0, len(saber_speed), slot_count)]

                # Encrypt each batch
                encrypted_batches = []
                for batch_index, batch in enumerate(batches):
                    print(f"Encoding batch {batch_index + 1}/{len(batches)} for file: {normalized_file}")
                    encoded_data = ckks_encoder.encode(batch, scale)  # Encode the batch
                    encrypted_data = encryptor.encrypt(encoded_data)  # Encrypt directly
                    encrypted_batches.append(encrypted_data)

                print(f"Encrypted {len(encrypted_batches)} batches successfully for file: {normalized_file}")

        # Verify by decrypting a sample
        print("Decrypting and verifying a sample from the last processed user...")
        decrypted_result = decryptor.decrypt(encrypted_batches[0])  # Decrypt the first batch
        decoded_result = ckks_encoder.decode(decrypted_result)  # Decode the plaintext
        print(f"Decrypted sample data: {decoded_result[:5]} (showing first 5 values)")

        print("Encryption completed successfully for all users!")
        return True

    except Exception as e:
        print(f"Error occurred during encryption: {e}")
        return False


# Path to chunk1 folder
chunk1_path = r"C:\Users\jguthula\Documents\chunk1"

# Run the encryption for all users
is_successful = encrypt_all_users(chunk1_path)
if is_successful:
    print("\nEncryption process completed for all users.")
else:
    print("\nEncryption process encountered errors.")
