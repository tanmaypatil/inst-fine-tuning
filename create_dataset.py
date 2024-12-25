import fitz
import os

def extract_text_from_pdf(pdf_path, from_page=None, to_page=None, output_dir=None):
    """
    Extract text from PDF file page by page with page range support
    
    Args:
        pdf_path (str): Path to PDF file
        from_page (int): Starting page number (1-based index). If None, starts from first page
        to_page (int): Ending page number (1-based index). If None, processes until last page
        output_dir (str): Directory to save extracted text files (optional)
    """
    try:
        # Open PDF file
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Handle default page range
        if from_page is None:
            from_page = 1
        if to_page is None:
            to_page = total_pages
            
        # Validate page range
        from_page = max(1, min(from_page, total_pages))  # Ensure from_page is between 1 and total_pages
        to_page = max(from_page, min(to_page, total_pages))  # Ensure to_page is between from_page and total_pages
        
        # Convert 1-based page numbers to 0-based indices
        from_index = from_page - 1
        to_index = to_page - 1
        
        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Process specified pages
        for page_num in range(from_index, to_index + 1):
            # Get the page
            page = doc[page_num]
            
            # Get page text
            text = page.get_text("text")  # Use 'text' mode for better formatting
            
            # If output directory is specified, save to file
            if output_dir:
                output_file = os.path.join(output_dir, f"page_{page_num + 1}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Extracted text from page {page_num + 1} saved to {output_file}")
            else:
                print(f"\nPage {page_num + 1}:")
                print("=" * 40)
                print(text)
                print("=" * 40)
        
        # Print summary
        print(f"\nProcessed pages {from_page} to {to_page} out of {total_pages} total pages")
        
        # Close the PDF
        doc.close()
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

# Example usage
if __name__ == "__main__":
    pdf_path = "india-today.pdf"  # Replace with your PDF path
    output_dir = "extracted_text"  # Optional: specify output directory
    

    # Example 2: Extract specific page range (e.g., pages 2 to 4)
    print("\nExample 2: Extracting pages 2 to 4")
    extract_text_from_pdf(pdf_path, from_page=1, to_page=1, output_dir=output_dir)
    
    
