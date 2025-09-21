"""
Core search system implementation for educational purposes.
This module contains the basic search system classes and utilities.
"""

from typing import List, Dict, Set, Optional, Tuple
import re
from collections import defaultdict, Counter
import math


class SearchSystem:
    """
    A more advanced search system with better ranking and query processing.
    """
    
    def __init__(self):
        self.products = []
        self.index = defaultdict(set)  # term -> set of product IDs
        self.term_frequencies = defaultdict(dict)  # term -> {product_id: frequency}
        self.document_frequencies = defaultdict(int)  # term -> number of documents containing it
        self.total_products = 0
    
    def add_product(self, product_id: str, title: str, description: str, 
                   category: str, price: float, brand: str, **kwargs):
        """Add a product to the search system with enhanced indexing."""
        product = {
            'id': product_id,
            'title': title,
            'description': description,
            'category': category,
            'price': price,
            'brand': brand,
            **kwargs
        }
        self.products.append(product)
        self.total_products += 1
        
        # Enhanced indexing with term frequency
        text = f"{title} {description} {category} {brand}".lower()
        terms = self._tokenize(text)
        
        # Count term frequencies in this document
        term_counts = Counter(terms)
        
        for term, count in term_counts.items():
            self.index[term].add(product_id)
            self.term_frequencies[term][product_id] = count
            self.document_frequencies[term] += 1
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into terms."""
        # Simple tokenization - in practice, you'd use more sophisticated methods
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        return [term for term in text.split() if len(term) > 1]
    
    def _calculate_tf_idf(self, term: str, product_id: str) -> float:
        """Calculate TF-IDF score for a term in a document."""
        if term not in self.term_frequencies or product_id not in self.term_frequencies[term]:
            return 0.0
        
        # Term frequency
        tf = self.term_frequencies[term][product_id]
        
        # Inverse document frequency
        idf = math.log(self.total_products / self.document_frequencies[term])
        
        return tf * idf
    
    def search(self, query: str, top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """Search for products with enhanced ranking."""
        query_terms = self._tokenize(query)
        
        if not query_terms:
            return []
        
        # Find matching products
        matching_products = set()
        for term in query_terms:
            matching_products.update(self.index.get(term, set()))
        
        # Calculate relevance scores
        results = []
        for product_id in matching_products:
            product = next(p for p in self.products if p['id'] == product_id)
            
            # Apply filters if provided
            if filters and not self._matches_filters(product, filters):
                continue
            
            # Calculate relevance score using TF-IDF
            relevance_score = sum(self._calculate_tf_idf(term, product_id) for term in query_terms)
            
            # Boost score for title matches
            title_boost = sum(1 for term in query_terms if term in product['title'].lower())
            relevance_score += title_boost * 0.5
            
            results.append({
                'product': product,
                'relevance_score': relevance_score
            })
        
        # Sort by relevance score and return top K
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:top_k]
    
    def _matches_filters(self, product: Dict, filters: Dict) -> bool:
        """Check if product matches the given filters."""
        for key, value in filters.items():
            if key == 'price_max' and product['price'] > value:
                return False
            elif key == 'price_min' and product['price'] < value:
                return False
            elif key == 'category' and product['category'] != value:
                return False
            elif key == 'brand' and product['brand'] != value:
                return False
        return True
    
    def get_suggestions(self, partial_query: str, max_suggestions: int = 5) -> List[str]:
        """Get query suggestions based on partial input."""
        partial_query = partial_query.lower()
        suggestions = set()
        
        for term in self.index.keys():
            if term.startswith(partial_query):
                suggestions.add(term)
        
        return sorted(list(suggestions))[:max_suggestions]
    
    def get_facets(self, query: str) -> Dict[str, List[Tuple[str, int]]]:
        """Get facet counts for the given query."""
        results = self.search(query, top_k=1000)  # Get more results for faceting
        
        facets = {
            'category': defaultdict(int),
            'brand': defaultdict(int),
            'price_range': defaultdict(int)
        }
        
        for result in results:
            product = result['product']
            
            # Category facets
            facets['category'][product['category']] += 1
            
            # Brand facets
            facets['brand'][product['brand']] += 1
            
            # Price range facets
            price = product['price']
            if price < 50:
                facets['price_range']['Under $50'] += 1
            elif price < 100:
                facets['price_range']['$50-$100'] += 1
            elif price < 500:
                facets['price_range']['$100-$500'] += 1
            else:
                facets['price_range']['Over $500'] += 1
        
        # Convert to sorted lists
        return {
            'category': sorted(facets['category'].items(), key=lambda x: x[1], reverse=True),
            'brand': sorted(facets['brand'].items(), key=lambda x: x[1], reverse=True),
            'price_range': sorted(facets['price_range'].items(), key=lambda x: x[1], reverse=True)
        }
