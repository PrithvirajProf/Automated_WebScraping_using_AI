import google.generativeai as genai
import os

# --- Configuration ---
# It's best practice to load your API key from an environment variable
# to keep it secure. Create an environment variable named 'GOOGLE_API_KEY'.
try:
    api_key = "AIzaSyBaKRyHxA6w47YGDJBTNH5VH-NeoGJ_ito"
    genai.configure(api_key=api_key)
except KeyError:
    print("🚨 GOOGLE_API_KEY environment variable not set.")
    print("Please set the environment variable to your Google AI Studio API key.")
    exit()


# --- Model and Prompt Template Initialization ---
model = genai.GenerativeModel('gemini-1.5-flash')

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_gemini(dom_chunks, parse_description):
    """
    Parses a list of text chunks using the Gemini model to extract specific information.

    Args:
        dom_chunks (list): A list of strings, where each string is a chunk of text to process.
        parse_description (str): A description of the information to extract.

    Returns:
        str: A single string with the extracted results from all chunks, joined by newlines.
    """
    parsed_results = []
    total_chunks = len(dom_chunks)

    print(f"Starting to process {total_chunks} chunk(s)...")

    for i, chunk in enumerate(dom_chunks, start=1):
        # Format the prompt with the current chunk and description
        prompt = template.format(dom_content=chunk, parse_description=parse_description)

        # Send the request to the Gemini API
        response = model.generate_content(prompt)

        # Append the model's response text to our results list
        try:
            parsed_results.append(response.text)
        except ValueError:
            # This can happen if the response is blocked due to safety settings
            print(f"⚠️ Warning: Received no valid content for chunk {i}. Appending an empty string.")
            parsed_results.append("")

        print(f"✅ Parsed chunk {i} of {total_chunks}")

    # Join all the individual results into a single string
    return "\n".join(parsed_results)

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Define the data chunks to be processed
    sample_dom_chunks = [
        "Product: Quantum Laptop, Price: $1200, Stock: 15 units. Description: A high-speed laptop for professionals.",
        "Contact us at support@example.com for help. Our phone number is (555) 123-4567.",
        "Product: Nebula Projector, Price: $800, Stock: 30 units. Not a laptop.",
    ]

    # 2. Define what you want to extract
    description_to_parse = "the name of any product that is a laptop"

    # 3. Call the function and get the result
    extracted_data = parse_with_gemini(sample_dom_chunks, description_to_parse)

    # 4. Print the final combined output
    print("\n--- Final Extracted Data ---")
    print(extracted_data)
    print("--------------------------")

    # --- Another Example ---
    description_to_parse_2 = "any email addresses"
    extracted_emails = parse_with_gemini(sample_dom_chunks, description_to_parse_2)
    print("\n--- Final Extracted Emails ---")
    print(extracted_emails)
    print("----------------------------")