from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TextSimilarityMerger:
    def __init__(self, similarity_threshold=0.3):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            max_df=0.95,
            min_df=2
        )
        self.similarity_threshold = similarity_threshold

    def read_files(self, file_paths):
        """Read content from multiple text files."""
        contents = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contents.append(file.read())
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                contents.append("")
        return contents

    def calculate_similarity_matrix(self, texts):
        """Calculate similarity matrix between all text pairs."""
        if not texts or all(not text.strip() for text in texts):
            return np.zeros((len(texts), len(texts)))

        # Transform texts to TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        return similarity_matrix

    def find_similar_pairs(self, similarity_matrix):
        """Find pairs of texts that are similar enough to be combined."""
        similar_pairs = []
        n_texts = len(similarity_matrix)
        
        for i in range(n_texts):
            for j in range(i + 1, n_texts):
                if similarity_matrix[i][j] >= self.similarity_threshold:
                    similar_pairs.append((i, j, similarity_matrix[i][j]))
        
        return sorted(similar_pairs, key=lambda x: x[2], reverse=True)

    def combine_texts(self, texts, similar_pairs):
        """Combine similar texts and return both combined and standalone texts."""
        if not similar_pairs:
            return texts, []

        combined_texts = []
        used_indices = set()
        
        for i, j, similarity in similar_pairs:
            if i not in used_indices and j not in used_indices:
                combined_text = f"Combined Text (Similarity: {similarity:.2f}):\n\n"
                combined_text += f"Text 1:\n{texts[i]}\n\n"
                combined_text += f"Text 2:\n{texts[j]}"
                combined_texts.append(combined_text)
                used_indices.add(i)
                used_indices.add(j)

        # Keep standalone texts
        standalone_texts = [text for idx, text in enumerate(texts) 
                          if idx not in used_indices]
        
        return standalone_texts, combined_texts

    def process_files(self, file_paths):
        """Main method to process multiple text files."""
        # Read all files
        texts = self.read_files(file_paths)
        
        # Calculate similarity matrix
        similarity_matrix = self.calculate_similarity_matrix(texts)
        
        # Find similar pairs
        similar_pairs = self.find_similar_pairs(similarity_matrix)
        
        # Combine similar texts and keep standalone ones
        standalone_texts, combined_texts = self.combine_texts(texts, similar_pairs)
        
        return standalone_texts, combined_texts

# Example usage
if __name__ == "__main__":
    # Initialize the merger with a similarity threshold
    merger = TextSimilarityMerger(similarity_threshold=0.3)
    
    # List of file paths
    file_paths = [
        "file1.txt",
        "file2.txt",
        "file3.txt"
    ]
    
    # Process the files
    standalone_texts, combined_texts = merger.process_files(file_paths)
    
    # Print results
    print("Combined Texts:")
    for i, text in enumerate(combined_texts, 1):
        print(f"\nCombined Text {i}:")
        print(text)
        print("-" * 80)
    
    print("\nStandalone Texts:")
    for i, text in enumerate(standalone_texts, 1):
        print(f"\nStandalone Text {i}:")
        print(text)
        print("-" * 80)