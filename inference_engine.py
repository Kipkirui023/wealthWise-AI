"""
Inference Engine for WealthWise AI
Processes financial data through knowledge base rules
"""

import math
from knowledge_base import FINANCIAL_RULES, get_retirement_benchmark

class WealthWiseInferenceEngine:
    def __init__(self):
        self.knowledge_base = FINANCIAL_RULES
        self.recommendations = []
        self.base_score = 100
        self.final_score = 100
        
    def evaluate_financial_health(self, user_data):
        """Main inference method using forward chaining"""
        self.recommendations = []
        self.final_score = self.base_score
        
        # Calculate derived metrics
        calculated_metrics = self._calculate_derived_metrics(user_data)
        user_data.update(calculated_metrics)
        
        # Apply all rules from knowledge base
        for category, ruleset in self.knowledge_base.items():
            category_applied = False
            
            for rule in ruleset['rules']:
                if self._evaluate_condition(rule['condition'], user_data):
                    # Apply score impact (weighted)
                    weighted_impact = rule['score_impact'] * ruleset['weight']
                    self.final_score += weighted_impact
                    
                    # Generate explanation with actual values
                    explanation = self._generate_explanation(rule, user_data)
                    
                    # Add recommendation
                    self.recommendations.append({
                        'category': category,
                        'message': rule['recommendation'],
                        'severity': rule['severity'],
                        'explanation': explanation,
                        'score_impact': weighted_impact,
                        'weight': ruleset['weight']
                    })
                    
                    category_applied = True
                    break  # Only apply first matching rule per category
            
            # If no rule matched for this category, add neutral feedback
            if not category_applied:
                self.recommendations.append({
                    'category': category,
                    'message': f"✅ {ruleset['description']} - No issues detected",
                    'severity': 'good',
                    'explanation': f"Your {ruleset['description'].lower()} appears to be in good standing",
                    'score_impact': 0,
                    'weight': ruleset['weight']
                })
        
        # Ensure score is within bounds
        self.final_score = max(0, min(100, self.final_score))
        
        return {
            'final_score': round(self.final_score),
            'grade': self._calculate_grade(self.final_score),
            'recommendations': self.recommendations,
            'metrics': calculated_metrics
        }
    
    def _calculate_derived_metrics(self, user_data):
        """Calculate derived financial metrics"""
        monthly_income = user_data['monthly_income']
        annual_income = monthly_income * 12
        
        metrics = {
            'debt_ratio': user_data['total_monthly_debt'] / monthly_income,
            'housing_ratio': user_data['housing_cost'] / monthly_income,
            'savings_rate': user_data['monthly_savings'] / monthly_income,
            'annual_income': annual_income,
            'age_benchmark': get_retirement_benchmark(user_data['age']),
            'coverage_months': user_data['emergency_savings'] / user_data['monthly_expenses']
        }
        
        return metrics
    
    def _evaluate_condition(self, condition, data):
        """Safely evaluate a condition string with data"""
        try:
            # Create a safe environment for eval
            safe_dict = {k: v for k, v in data.items() if not k.startswith('_')}
            return eval(condition, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            print(f"Error evaluating condition: {condition} - {e}")
            return False
    
    def _generate_explanation(self, rule, user_data):
        """Generate natural language explanation for recommendations"""
        try:
            # Use the template from the rule
            if 'explanation_template' in rule:
                explanation = rule['explanation_template'].format(**user_data)
            else:
                explanation = "Based on standard financial planning guidelines"
            
            return explanation
        except Exception as e:
            return "Based on analysis of your financial situation"
    
    def _calculate_grade(self, score):
        """Convert numerical score to letter grade"""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        elif score >= 50: return "C-"
        elif score >= 40: return "D"
        else: return "F"
    
    def get_recommendations_by_priority(self):
        """Sort recommendations by severity priority"""
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'good': 3, 'excellent': 4}
        return sorted(self.recommendations, key=lambda x: priority_order.get(x['severity'], 5))