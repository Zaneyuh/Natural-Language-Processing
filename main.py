def translate_to_english(text):
    return "TEST ENGLISH TRANSLATION"


def get_medical_response(text):
    return "TEST MEDICAL RESPONSE"


def translate_to_cebuano(text):
    return "TEST CEBUANO RESPONSE"


def main():
    print("====================================")
    print("          CEBUANO DOCTOR")
    print("====================================")
    print("Disclaimer: This chatbot is for educational purposes only.")
    print("It is not a substitute for professional medical advice.")

    while True:
        print("\nEnter a Cebuano healthcare question.")
        query = input("> ").strip()

        if not query:
            print("Please enter a valid question.")
            continue

        try:
            print("\n[1/3] Translating Cebuano to English...")
            english_query = translate_to_english(query)

            print("[2/3] Generating medical response...")
            medical_response = get_medical_response(english_query)

            print("[3/3] Translating response to Cebuano...")
            cebuano_response = translate_to_cebuano(medical_response)

            print("\n------------------------------------")
            print("Original Cebuano Question:")
            print(query)

            print("\n------------------------------------")
            print("English Translation:")
            print(english_query)

            print("\n------------------------------------")
            print("Medical Response:")
            print(medical_response)

            print("\n------------------------------------")
            print("Final Cebuano Response:")
            print(cebuano_response)

            print("------------------------------------")

        except Exception as e:
            print("\nAn error occurred while processing the request.")
            print(f"Error: {e}")

        again = input("\nAsk another question? [Y/N]: ").strip()

        if again.lower() != "y":
            print("\nThank you for using Cebuano Doctor!")
            break


if __name__ == "__main__":
    main()