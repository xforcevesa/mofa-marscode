from typing import List
from openai import OpenAI
from .shopping_result import HtmlSearchText
import tiktoken

prompt_template="""
# Prompt for Product Information Extraction

## Backstory
You are an AI agent designed to extract relevant product information from HTML cards. These cards are part of a shopping site's web pages that display search results based on specific keywords.

## Objective
Parse the provided HTML content and extract all information related to products from their containers or elements accurately and comprehensively.

## Specifics
- Extract all relevant product details such as:
  - Titles
  - Descriptions
  - Prices
  - Images
  - Links
  - Specifications
  - Any other attributes directly related to the product.
- Preserve the original sequence of the HTML elements as they appear in the document.
- Exclude irrelevant elements such as advertisements, navigation menus, or any unrelated content.

## Tasks
1. Analyze the HTML structure to locate product-related containers or elements.
2. Identify and extract product information such as titles, descriptions, images, prices, links, etc.
3. Organize the extracted data to maintain the sequence as found in the HTML source.
4. Format the extracted content in a structured and machine-readable way for further processing.

---

### Input Data
#### HTML Source
`{html_content}`
#### Search Keyword
`{search_text}`

"""

class ProductAnalysisAgent:
    def __init__(self, api_key: str,):
        """
        Initialize the ProductAnalysisAgent.

        Args:
            api_key (str): API key for the model.
            base_url (str): Base URL for the API.
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key, )

    def estimate_card_tokens(self, card_html: str, model: str = "gpt-4") -> int:
        """
        Estimate the token count of a single HTML card.

        Args:
            card_html (str): HTML content of a card.
            model (str): Model name for encoding.

        Returns:
            int: Estimated token count.
        """
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(card_html))

    def process_cards(
        self, 
        cards: List[str], 
        model_name: str, 
        max_tokens: int, 
        prompt_template: str, 
        key_word: str, 
        redundancy: int = 1000
    ) -> HtmlSearchText:
        """
        Process a list of cards and return parsed product information for all cards.

        Args:
            cards (List[str]): List of HTML cards.
            model_name (str): Name of the model to use.
            max_tokens (int): Maximum token limit for the model.
            prompt_template (str): Template for the LLM prompt.
            key_word (str): Search key word.
            redundancy (int): Reserved token count for safety margin.
        Returns:
            HtmlSearchText: Parsed product information.
        """
        if not cards:
            raise ValueError("No cards provided for processing.")

        # Estimate tokens per card and per prompt
        estimated_card_tokens = self.estimate_card_tokens(cards[0])
        estimated_prompt_tokens = self.estimate_card_tokens(prompt_template)
        max_cards_per_batch = (max_tokens - estimated_prompt_tokens - redundancy) // estimated_card_tokens
        
        # Calculate total batches
        total_batches = (len(cards) + max_cards_per_batch - 1) // max_cards_per_batch  # Ceiling division for batches

        print(f"[INFO] Estimated tokens per card: {estimated_card_tokens}")
        print(f"[INFO] Max cards that fit within token limit per batch: {max_cards_per_batch}")
        print(f"[INFO] Estimated total number of batches to process: {total_batches}")
        
        all_results = []
        while len(all_results) < len(cards):
            remaining_cards = cards[len(all_results):]
            batch_cards = remaining_cards[:max_cards_per_batch]
            print(f"[INFO] Processing batch starting at card {len(all_results) + 1} with {len(batch_cards)} cards.")
            
            prompt = prompt_template.format(html_content="\n".join(batch_cards), search_text=key_word)

            try:
                response = self.client.beta.chat.completions.parse(
                    model=model_name,  
                    messages=[{"role": "user", "content": prompt}],
                    response_format=HtmlSearchText,
                )
                batch_results = response.choices[0].message.parsed
                all_results.extend(batch_results.chunks or [])
                print(f"[INFO] Successfully processed up to card {len(all_results)}.")
                # print(batch_results)
            except Exception as e:
                print(f"[ERROR] Failed to process batch starting at card {len(all_results) + 1}: {str(e)}")
                # Optionally retry logic for failed batch could be implemented here

        return HtmlSearchText(chunks=all_results)
