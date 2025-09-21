"""
Search and recommendation system metrics for evaluation.
"""

from typing import List, Dict, Set, Optional
import numpy as np
from collections import defaultdict


class SearchMetrics:
    """Calculate various search quality metrics."""
    
    @staticmethod
    def precision_at_k(relevant_items: Set[str], retrieved_items: List[str], k: int) -> float:
        """Calculate Precision@K."""
        if k == 0 or not retrieved_items:
            return 0.0
        
        relevant_retrieved = set(retrieved_items[:k]) & relevant_items
        return len(relevant_retrieved) / min(k, len(retrieved_items))
    
    @staticmethod
    def recall_at_k(relevant_items: Set[str], retrieved_items: List[str], k: int) -> float:
        """Calculate Recall@K."""
        if not relevant_items:
            return 0.0
        
        relevant_retrieved = set(retrieved_items[:k]) & relevant_items
        return len(relevant_retrieved) / len(relevant_items)
    
    @staticmethod
    def ndcg_at_k(relevant_items: Set[str], retrieved_items: List[str], k: int) -> float:
        """Calculate Normalized Discounted Cumulative Gain@K."""
        if k == 0 or not retrieved_items:
            return 0.0
        
        # Calculate DCG
        dcg = 0.0
        for i, item in enumerate(retrieved_items[:k]):
            if item in relevant_items:
                dcg += 1.0 / np.log2(i + 2)  # i+2 because log2(1) = 0
        
        # Calculate IDCG (ideal DCG)
        idcg = 0.0
        for i in range(min(k, len(relevant_items))):
            idcg += 1.0 / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0.0
    
    @staticmethod
    def mean_reciprocal_rank(relevant_items: Set[str], retrieved_items: List[str]) -> float:
        """Calculate Mean Reciprocal Rank."""
        if not relevant_items or not retrieved_items:
            return 0.0
        
        for i, item in enumerate(retrieved_items):
            if item in relevant_items:
                return 1.0 / (i + 1)
        
        return 0.0
    
    @staticmethod
    def calculate_all_metrics(relevant_items: Set[str], retrieved_items: List[str], 
                            k_values: List[int] = [1, 3, 5, 10]) -> Dict[str, float]:
        """Calculate all metrics for a single query."""
        metrics = {}
        
        for k in k_values:
            metrics[f'precision_at_{k}'] = SearchMetrics.precision_at_k(
                relevant_items, retrieved_items, k)
            metrics[f'recall_at_{k}'] = SearchMetrics.recall_at_k(
                relevant_items, retrieved_items, k)
            metrics[f'ndcg_at_{k}'] = SearchMetrics.ndcg_at_k(
                relevant_items, retrieved_items, k)
        
        metrics['mrr'] = SearchMetrics.mean_reciprocal_rank(relevant_items, retrieved_items)
        
        return metrics


class BusinessMetrics:
    """Calculate business impact metrics."""
    
    @staticmethod
    def click_through_rate(clicks: int, impressions: int) -> float:
        """Calculate Click-Through Rate."""
        return clicks / impressions if impressions > 0 else 0.0
    
    @staticmethod
    def conversion_rate(purchases: int, searches: int) -> float:
        """Calculate Search-to-Purchase Conversion Rate."""
        return purchases / searches if searches > 0 else 0.0
    
    @staticmethod
    def revenue_per_search(revenue: float, searches: int) -> float:
        """Calculate Revenue per Search."""
        return revenue / searches if searches > 0 else 0.0
    
    @staticmethod
    def average_order_value(revenue: float, orders: int) -> float:
        """Calculate Average Order Value."""
        return revenue / orders if orders > 0 else 0.0


class A_B_Testing:
    """A/B testing utilities for search experiments."""
    
    @staticmethod
    def calculate_sample_size(baseline_rate: float, minimum_detectable_effect: float, 
                            power: float = 0.8, alpha: float = 0.05) -> int:
        """Calculate required sample size for A/B test."""
        from scipy import stats
        
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        p1 = baseline_rate
        p2 = baseline_rate + minimum_detectable_effect
        
        n = ((z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))) / ((p1 - p2) ** 2)
        
        return int(np.ceil(n))
    
    @staticmethod
    def chi_square_test(control_conversions: int, control_trials: int,
                       treatment_conversions: int, treatment_trials: int) -> Dict:
        """Perform chi-square test for A/B testing."""
        from scipy.stats import chi2_contingency
        
        # Create contingency table
        contingency_table = [
            [control_conversions, control_trials - control_conversions],
            [treatment_conversions, treatment_trials - treatment_conversions]
        ]
        
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        
        # Calculate conversion rates
        control_rate = control_conversions / control_trials if control_trials > 0 else 0
        treatment_rate = treatment_conversions / treatment_trials if treatment_trials > 0 else 0
        
        # Calculate lift
        lift = (treatment_rate - control_rate) / control_rate if control_rate > 0 else 0
        
        return {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'control_rate': control_rate,
            'treatment_rate': treatment_rate,
            'lift': lift,
            'is_significant': p_value < 0.05
        }
