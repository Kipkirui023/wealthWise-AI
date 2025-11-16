"""
Knowledge Base for WealthWise AI
Contains all financial rules and expert knowledge
"""

FINANCIAL_RULES = {
    "emergency_fund": {
        "description": "Emergency savings adequacy",
        "weight": 0.25,  # 25% of total score
        "rules": [
            {
                "condition": "emergency_savings < (3 * monthly_expenses)",
                "score_impact": -20,
                "recommendation": "🚨 PRIORITY: Build emergency fund to cover 3-6 months of expenses",
                "severity": "high",
                "explanation_template": "Your emergency savings (${emergency_savings}) should cover 3-6 months of expenses (${monthly_expenses} × 3 = ${3 * monthly_expenses})"
            },
            {
                "condition": "emergency_savings >= (3 * monthly_expenses) and emergency_savings < (6 * monthly_expenses)",
                "score_impact": 0,
                "recommendation": "✅ Good! Consider building to 6 months for extra security",
                "severity": "good",
                "explanation_template": "Your emergency fund covers {coverage_months:.1f} months of expenses - within the recommended 3-6 month range"
            },
            {
                "condition": "emergency_savings >= (6 * monthly_expenses)",
                "score_impact": 15,
                "recommendation": "🎉 Excellent! Your emergency fund is robust",
                "severity": "excellent",
                "explanation_template": "Your emergency fund covers {coverage_months:.1f} months - excellent financial security!"
            }
        ]
    },
    
    "debt_to_income": {
        "description": "Debt burden assessment",
        "weight": 0.25,
        "rules": [
            {
                "condition": "debt_ratio > 0.40",
                "score_impact": -25,
                "recommendation": "🚨 CRITICAL: Your debt burden is very high! Focus on debt reduction immediately",
                "severity": "critical",
                "explanation_template": "Your debt-to-income ratio is {debt_ratio:.1%} (should be < 36%)"
            },
            {
                "condition": "debt_ratio > 0.36 and debt_ratio <= 0.40",
                "score_impact": -15,
                "recommendation": "⚠️ High debt burden! Focus on debt reduction strategies",
                "severity": "high",
                "explanation_template": "Your debt-to-income ratio is {debt_ratio:.1%} (should be < 36%)"
            },
            {
                "condition": "debt_ratio > 0.20 and debt_ratio <= 0.36",
                "score_impact": -5,
                "recommendation": "ℹ️ Manageable debt level, but keep monitoring",
                "severity": "medium",
                "explanation_template": "Your debt-to-income ratio is {debt_ratio:.1%} - close to the recommended 36% maximum"
            },
            {
                "condition": "debt_ratio <= 0.20",
                "score_impact": 15,
                "recommendation": "✅ Excellent debt management!",
                "severity": "excellent",
                "explanation_template": "Your debt-to-income ratio is {debt_ratio:.1%} - well below the 36% guideline!"
            }
        ]
    },
    
    "housing_cost": {
        "description": "Housing affordability",
        "weight": 0.15,
        "rules": [
            {
                "condition": "housing_ratio > 0.35",
                "score_impact": -15,
                "recommendation": "🏠 Housing cost is too high! Consider downsizing or increasing income",
                "severity": "high",
                "explanation_template": "Your housing cost (${housing_cost}) is {housing_ratio:.1%} of income (recommended: < 30%)"
            },
            {
                "condition": "housing_ratio > 0.30 and housing_ratio <= 0.35",
                "score_impact": -5,
                "recommendation": "🏠 Housing cost is slightly high. Monitor this closely",
                "severity": "medium",
                "explanation_template": "Your housing cost (${housing_cost}) is {housing_ratio:.1%} of income (recommended: < 30%)"
            },
            {
                "condition": "housing_ratio <= 0.30",
                "score_impact": 10,
                "recommendation": "✅ Housing costs are within healthy range",
                "severity": "good",
                "explanation_template": "Your housing cost (${housing_cost}) is {housing_ratio:.1%} of income - within the recommended 30% guideline"
            }
        ]
    },
    
    "savings_rate": {
        "description": "Overall savings habit",
        "weight": 0.20,
        "rules": [
            {
                "condition": "savings_rate < 0.05",
                "score_impact": -15,
                "recommendation": "💸 Very low savings rate! Aim to save at least 10-20% of income",
                "severity": "high",
                "explanation_template": "Your savings rate is {savings_rate:.1%} (recommended: 20% for financial freedom)"
            },
            {
                "condition": "savings_rate >= 0.05 and savings_rate < 0.10",
                "score_impact": -8,
                "recommendation": "💸 Low savings rate. Work toward saving 15-20% of income",
                "severity": "medium",
                "explanation_template": "Your savings rate is {savings_rate:.1%} (recommended: 20% for financial freedom)"
            },
            {
                "condition": "savings_rate >= 0.10 and savings_rate < 0.20",
                "score_impact": 5,
                "recommendation": "✅ Good savings habit. Try to reach 20%",
                "severity": "good",
                "explanation_template": "Your savings rate is {savings_rate:.1%} - good progress toward the 20% goal"
            },
            {
                "condition": "savings_rate >= 0.20",
                "score_impact": 15,
                "recommendation": "🎉 Outstanding savings rate! You're building wealth effectively",
                "severity": "excellent",
                "explanation_template": "Your savings rate is {savings_rate:.1%} - excellent wealth-building habit!"
            }
        ]
    },
    
    "retirement_savings": {
        "description": "Retirement planning adequacy",
        "weight": 0.15,
        "rules": [
            {
                "condition": "age < 30 and retirement_savings < (0.5 * annual_income)",
                "score_impact": -8,
                "recommendation": "💰 Start retirement savings now! Aim to have 1x annual salary by age 30",
                "severity": "medium",
                "explanation_template": "You have ${retirement_savings} saved (recommended: ${0.5 * annual_income} by age {age})"
            },
            {
                "condition": "age >= 30 and age < 40 and retirement_savings < (1 * annual_income)",
                "score_impact": -12,
                "recommendation": "💰 Boost retirement contributions to catch up to age-based benchmarks",
                "severity": "high",
                "explanation_template": "You have ${retirement_savings} saved (recommended: ${1 * annual_income} by age {age})"
            },
            {
                "condition": "age >= 40 and retirement_savings < (3 * annual_income)",
                "score_impact": -15,
                "recommendation": "💰 Significant retirement savings gap. Consider increasing contributions",
                "severity": "high",
                "explanation_template": "You have ${retirement_savings} saved (recommended: ${3 * annual_income} by age {age})"
            },
            {
                "condition": "retirement_savings >= (age_benchmark * annual_income)",
                "score_impact": 12,
                "recommendation": "✅ Excellent retirement planning! You're on track for retirement",
                "severity": "excellent",
                "explanation_template": "You have ${retirement_savings} saved - meeting age {age} benchmark of {age_benchmark}x annual income!"
            }
        ]
    }
}

def get_retirement_benchmark(age):
    """Get retirement savings benchmark based on age"""
    if age < 30:
        return 0.5
    elif age < 40:
        return 1.0
    elif age < 50:
        return 3.0
    elif age < 60:
        return 6.0
    else:
        return 8.0